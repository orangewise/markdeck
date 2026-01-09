"""Tests for the image diff tool."""

import tempfile
import unittest
from pathlib import Path

try:
    from PIL import Image

    from image_diff import ImageDiffer

    DEPENDENCIES_AVAILABLE = True
except ImportError:
    DEPENDENCIES_AVAILABLE = False


def create_test_image(path: Path, size: tuple = (100, 100), color: tuple = (255, 0, 0, 255)):
    """
    Create a simple test image.

    Args:
        path: Path where to save the image
        size: Image dimensions (width, height)
        color: RGBA color tuple
    """
    img = Image.new("RGBA", size, color)
    img.save(path)


def create_different_image(path: Path, size: tuple = (100, 100)):
    """
    Create a test image with some differences.

    Args:
        path: Path where to save the image
        size: Image dimensions (width, height)
    """
    img = Image.new("RGBA", size, (255, 0, 0, 255))
    # Add a white square in the center to create differences
    pixels = img.load()
    for x in range(40, 60):
        for y in range(40, 60):
            pixels[x, y] = (255, 255, 255, 255)
    img.save(path)


@unittest.skipIf(not DEPENDENCIES_AVAILABLE, "pixelmatch and Pillow not installed")
class TestImageDiffer(unittest.TestCase):
    """Test the ImageDiffer class."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()

    def test_initialization(self):
        """Test ImageDiffer initialization with default parameters."""
        differ = ImageDiffer()
        self.assertEqual(differ.threshold, 0.1)
        self.assertEqual(differ.include_anti_aliasing, True)

    def test_initialization_custom_params(self):
        """Test ImageDiffer initialization with custom parameters."""
        differ = ImageDiffer(threshold=0.05, include_anti_aliasing=False)
        self.assertEqual(differ.threshold, 0.05)
        self.assertEqual(differ.include_anti_aliasing, False)

    def test_compare_identical_images(self):
        """Test comparing two identical images."""
        img_path = self.temp_path / "test.png"
        create_test_image(img_path)

        differ = ImageDiffer()
        mismatch, total, percentage, match = differ.compare(img_path, img_path)

        self.assertEqual(mismatch, 0)
        self.assertEqual(total, 10000)  # 100x100 pixels
        self.assertEqual(percentage, 0.0)
        self.assertTrue(match)

    def test_compare_different_images(self):
        """Test comparing two different images."""
        img1_path = self.temp_path / "img1.png"
        img2_path = self.temp_path / "img2.png"

        create_test_image(img1_path, color=(255, 0, 0, 255))  # Red
        create_test_image(img2_path, color=(0, 0, 255, 255))  # Blue

        differ = ImageDiffer()
        mismatch, total, percentage, match = differ.compare(img1_path, img2_path)

        self.assertGreater(mismatch, 0)
        self.assertEqual(total, 10000)
        self.assertGreater(percentage, 0)
        self.assertFalse(match)

    def test_compare_with_diff_output(self):
        """Test comparing images and generating diff output."""
        img1_path = self.temp_path / "img1.png"
        img2_path = self.temp_path / "img2.png"
        diff_path = self.temp_path / "diff.png"

        create_test_image(img1_path)
        create_different_image(img2_path)

        differ = ImageDiffer()
        mismatch, total, percentage, match = differ.compare(img1_path, img2_path, diff_path)

        self.assertGreater(mismatch, 0)
        self.assertFalse(match)
        self.assertTrue(diff_path.exists())
        self.assertGreater(diff_path.stat().st_size, 0)

    def test_compare_with_subdirectory_creation(self):
        """Test that diff output creates necessary subdirectories."""
        img1_path = self.temp_path / "img1.png"
        img2_path = self.temp_path / "img2.png"
        diff_path = self.temp_path / "subdir" / "nested" / "diff.png"

        create_test_image(img1_path)
        create_different_image(img2_path)

        differ = ImageDiffer()
        differ.compare(img1_path, img2_path, diff_path)

        self.assertTrue(diff_path.exists())
        self.assertTrue(diff_path.parent.exists())

    def test_compare_missing_first_image(self):
        """Test comparing when first image doesn't exist."""
        img1_path = self.temp_path / "nonexistent.png"
        img2_path = self.temp_path / "img2.png"
        create_test_image(img2_path)

        differ = ImageDiffer()
        with self.assertRaises(FileNotFoundError) as ctx:
            differ.compare(img1_path, img2_path)

        self.assertIn("nonexistent.png", str(ctx.exception))

    def test_compare_missing_second_image(self):
        """Test comparing when second image doesn't exist."""
        img1_path = self.temp_path / "img1.png"
        img2_path = self.temp_path / "nonexistent.png"
        create_test_image(img1_path)

        differ = ImageDiffer()
        with self.assertRaises(FileNotFoundError) as ctx:
            differ.compare(img1_path, img2_path)

        self.assertIn("nonexistent.png", str(ctx.exception))

    def test_compare_different_dimensions(self):
        """Test comparing images with different dimensions."""
        img1_path = self.temp_path / "img1.png"
        img2_path = self.temp_path / "img2.png"

        create_test_image(img1_path, size=(100, 100))
        create_test_image(img2_path, size=(200, 200))

        differ = ImageDiffer()
        with self.assertRaises(ValueError) as ctx:
            differ.compare(img1_path, img2_path)

        self.assertIn("dimensions don't match", str(ctx.exception))
        self.assertIn("100, 100", str(ctx.exception))
        self.assertIn("200, 200", str(ctx.exception))

    def test_compare_with_custom_threshold(self):
        """Test comparing with custom threshold parameter."""
        img1_path = self.temp_path / "img1.png"
        img2_path = self.temp_path / "img2.png"

        create_test_image(img1_path)
        create_different_image(img2_path)

        # More sensitive threshold
        differ_sensitive = ImageDiffer(threshold=0.01)
        mismatch_sensitive, _, _, _ = differ_sensitive.compare(img1_path, img2_path)

        # Less sensitive threshold
        differ_tolerant = ImageDiffer(threshold=0.5)
        mismatch_tolerant, _, _, _ = differ_tolerant.compare(img1_path, img2_path)

        # More sensitive should detect more or equal differences
        self.assertGreaterEqual(mismatch_sensitive, mismatch_tolerant)

    def test_compare_with_string_paths(self):
        """Test that compare accepts string paths."""
        img_path = self.temp_path / "test.png"
        create_test_image(img_path)

        differ = ImageDiffer()
        mismatch, total, percentage, match = differ.compare(str(img_path), str(img_path))

        self.assertEqual(mismatch, 0)
        self.assertTrue(match)


@unittest.skipIf(not DEPENDENCIES_AVAILABLE, "pixelmatch and Pillow not installed")
class TestImageDifferDirectory(unittest.TestCase):
    """Test the ImageDiffer directory comparison."""

    def setUp(self):
        """Set up test environment with directories."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        self.dir1 = self.temp_path / "dir1"
        self.dir2 = self.temp_path / "dir2"
        self.diff_dir = self.temp_path / "diffs"

        self.dir1.mkdir()
        self.dir2.mkdir()

    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()

    def test_compare_directory_identical(self):
        """Test comparing directories with identical images."""
        # Create identical images in both directories
        for i in range(3):
            img_path1 = self.dir1 / f"image{i}.png"
            img_path2 = self.dir2 / f"image{i}.png"
            create_test_image(img_path1)
            create_test_image(img_path2)

        differ = ImageDiffer()
        results = differ.compare_directory(self.dir1, self.dir2)

        self.assertEqual(len(results), 3)
        for filename, result in results.items():
            self.assertEqual(result["status"], "identical")
            self.assertEqual(result["diff_pixels"], 0)
            self.assertEqual(result["diff_percentage"], 0.0)

    def test_compare_directory_different(self):
        """Test comparing directories with different images."""
        # Create different images in both directories
        for i in range(2):
            img_path1 = self.dir1 / f"image{i}.png"
            img_path2 = self.dir2 / f"image{i}.png"
            create_test_image(img_path1)
            create_different_image(img_path2)

        differ = ImageDiffer()
        results = differ.compare_directory(self.dir1, self.dir2)

        self.assertEqual(len(results), 2)
        for filename, result in results.items():
            self.assertEqual(result["status"], "different")
            self.assertGreater(result["diff_pixels"], 0)
            self.assertGreater(result["diff_percentage"], 0)

    def test_compare_directory_with_diff_output(self):
        """Test comparing directories and saving diff images."""
        # Create different images
        img_path1 = self.dir1 / "test.png"
        img_path2 = self.dir2 / "test.png"
        create_test_image(img_path1)
        create_different_image(img_path2)

        differ = ImageDiffer()
        results = differ.compare_directory(self.dir1, self.dir2, self.diff_dir)

        self.assertEqual(len(results), 1)
        result = results["test.png"]
        self.assertEqual(result["status"], "different")
        self.assertIsNotNone(result["diff_image"])

        diff_path = Path(result["diff_image"])
        self.assertTrue(diff_path.exists())
        self.assertIn("diff_test.png", str(diff_path))

    def test_compare_directory_missing_file(self):
        """Test comparing directories when file missing in second directory."""
        # Create image only in first directory
        img_path1 = self.dir1 / "only_in_dir1.png"
        create_test_image(img_path1)

        differ = ImageDiffer()
        results = differ.compare_directory(self.dir1, self.dir2)

        self.assertEqual(len(results), 1)
        result = results["only_in_dir1.png"]
        self.assertEqual(result["status"], "missing_in_dir2")
        self.assertIn("error", result)

    def test_compare_directory_with_pattern(self):
        """Test comparing directories with custom file pattern."""
        # Create PNG and JPG files
        create_test_image(self.dir1 / "image1.png")
        create_test_image(self.dir1 / "image2.png")
        create_test_image(self.dir1 / "image3.jpg")

        create_test_image(self.dir2 / "image1.png")
        create_test_image(self.dir2 / "image2.png")
        create_test_image(self.dir2 / "image3.jpg")

        differ = ImageDiffer()
        # Only compare PNG files
        results = differ.compare_directory(self.dir1, self.dir2, pattern="*.png")

        self.assertEqual(len(results), 2)
        self.assertIn("image1.png", results)
        self.assertIn("image2.png", results)
        self.assertNotIn("image3.jpg", results)

    def test_compare_directory_with_errors(self):
        """Test comparing directories with dimension mismatch."""
        # Create images with different dimensions
        img_path1 = self.dir1 / "test.png"
        img_path2 = self.dir2 / "test.png"
        create_test_image(img_path1, size=(100, 100))
        create_test_image(img_path2, size=(200, 200))

        differ = ImageDiffer()
        results = differ.compare_directory(self.dir1, self.dir2)

        self.assertEqual(len(results), 1)
        result = results["test.png"]
        self.assertEqual(result["status"], "error")
        self.assertIn("error", result)

    def test_compare_directory_empty(self):
        """Test comparing empty directories."""
        differ = ImageDiffer()
        results = differ.compare_directory(self.dir1, self.dir2)

        self.assertEqual(len(results), 0)

    def test_compare_directory_with_string_paths(self):
        """Test that compare_directory accepts string paths."""
        img_path1 = self.dir1 / "test.png"
        img_path2 = self.dir2 / "test.png"
        create_test_image(img_path1)
        create_test_image(img_path2)

        differ = ImageDiffer()
        results = differ.compare_directory(str(self.dir1), str(self.dir2))

        self.assertEqual(len(results), 1)
        self.assertEqual(results["test.png"]["status"], "identical")

    def test_compare_directory_creates_output_dir(self):
        """Test that compare_directory creates output directory if needed."""
        img_path1 = self.dir1 / "test.png"
        img_path2 = self.dir2 / "test.png"
        create_test_image(img_path1)
        create_different_image(img_path2)

        # Output directory doesn't exist yet
        output_dir = self.temp_path / "new_diffs"
        self.assertFalse(output_dir.exists())

        differ = ImageDiffer()
        results = differ.compare_directory(self.dir1, self.dir2, output_dir)

        self.assertTrue(output_dir.exists())
        self.assertEqual(results["test.png"]["status"], "different")


@unittest.skipIf(not DEPENDENCIES_AVAILABLE, "pixelmatch and Pillow not installed")
class TestImageDifferEdgeCases(unittest.TestCase):
    """Test edge cases for ImageDiffer."""

    def setUp(self):
        """Set up test environment."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

    def tearDown(self):
        """Clean up test environment."""
        self.temp_dir.cleanup()

    def test_compare_small_image(self):
        """Test comparing very small images."""
        img1_path = self.temp_path / "small1.png"
        img2_path = self.temp_path / "small2.png"

        create_test_image(img1_path, size=(1, 1))
        create_test_image(img2_path, size=(1, 1))

        differ = ImageDiffer()
        mismatch, total, percentage, match = differ.compare(img1_path, img2_path)

        self.assertEqual(total, 1)
        self.assertTrue(match)

    def test_compare_large_dimensions(self):
        """Test comparing larger images."""
        img1_path = self.temp_path / "large1.png"
        img2_path = self.temp_path / "large2.png"

        create_test_image(img1_path, size=(500, 500))
        create_test_image(img2_path, size=(500, 500))

        differ = ImageDiffer()
        mismatch, total, percentage, match = differ.compare(img1_path, img2_path)

        self.assertEqual(total, 250000)  # 500x500
        self.assertTrue(match)

    def test_compare_with_transparency(self):
        """Test comparing images with different transparency."""
        img1_path = self.temp_path / "img1.png"
        img2_path = self.temp_path / "img2.png"

        create_test_image(img1_path, color=(255, 0, 0, 255))  # Fully opaque red
        create_test_image(img2_path, color=(255, 0, 0, 128))  # Semi-transparent red

        differ = ImageDiffer()
        mismatch, total, percentage, match = differ.compare(img1_path, img2_path)

        self.assertGreater(mismatch, 0)
        self.assertFalse(match)


if __name__ == "__main__":
    unittest.main()
