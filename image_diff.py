#!/usr/bin/env python3
"""
Visual image diff tool for MarkDeck screenshots.

Compares two images and generates a visual diff highlighting changed pixels.
Uses pixelmatch algorithm to detect and visualize differences.
"""

import sys
from pathlib import Path

try:
    from PIL import Image
    from pixelmatch.contrib.PIL import pixelmatch
except ImportError:
    print("Error: Required dependencies not installed.")
    print("Install with: uv pip install pixelmatch Pillow --python .venv/bin/python")
    sys.exit(1)


class ImageDiffer:
    """Compare images and generate visual diffs."""

    def __init__(self, threshold: float = 0.1, include_anti_aliasing: bool = True):
        """
        Initialize ImageDiffer.

        Args:
            threshold: Matching threshold (0-1). Smaller = more sensitive.
                      0.1 is recommended for screenshots with slight rendering differences.
            include_anti_aliasing: If True, detects anti-aliasing differences.
                                  Set to False to ignore minor anti-aliasing changes.
        """
        self.threshold = threshold
        self.include_anti_aliasing = include_anti_aliasing

    def compare(
        self,
        img1_path: str | Path,
        img2_path: str | Path,
        diff_output_path: str | Path | None = None,
        diff_color: tuple = (255, 0, 128),  # Pink/magenta
    ) -> tuple[int, int, float, bool]:
        """
        Compare two images and optionally create a visual diff.

        Args:
            img1_path: Path to first image (reference/old)
            img2_path: Path to second image (new)
            diff_output_path: Optional path to save diff image.
                            If None, no diff image is created.
            diff_color: RGB color for highlighting differences (default: pink)

        Returns:
            Tuple of (num_diff_pixels, total_pixels, diff_percentage, images_match)

        Raises:
            FileNotFoundError: If either image doesn't exist
            ValueError: If images have different dimensions
        """
        img1_path = Path(img1_path)
        img2_path = Path(img2_path)

        # Validate inputs
        if not img1_path.exists():
            raise FileNotFoundError(f"Image not found: {img1_path}")
        if not img2_path.exists():
            raise FileNotFoundError(f"Image not found: {img2_path}")

        # Load images
        img1 = Image.open(img1_path).convert("RGBA")
        img2 = Image.open(img2_path).convert("RGBA")

        # Check dimensions match
        if img1.size != img2.size:
            raise ValueError(
                f"Image dimensions don't match: {img1.size} vs {img2.size}. "
                "Both images must have the same dimensions."
            )

        # Create diff image
        img_diff = Image.new("RGBA", img1.size)

        # Compare and generate visual diff
        mismatch = pixelmatch(
            img1,
            img2,
            img_diff,
            threshold=self.threshold,
            includeAA=self.include_anti_aliasing,
            diff_color=diff_color,
        )

        # Calculate statistics
        total_pixels = img1.width * img1.height
        diff_percentage = (mismatch / total_pixels) * 100
        images_match = mismatch == 0

        # Save diff image if requested
        if diff_output_path:
            diff_output_path = Path(diff_output_path)
            diff_output_path.parent.mkdir(parents=True, exist_ok=True)
            img_diff.save(diff_output_path)

        return mismatch, total_pixels, diff_percentage, images_match

    def compare_directory(
        self,
        dir1: str | Path,
        dir2: str | Path,
        diff_output_dir: str | Path | None = None,
        pattern: str = "*.png",
    ) -> dict:
        """
        Compare all matching images in two directories.

        Args:
            dir1: First directory (reference/old)
            dir2: Second directory (new)
            diff_output_dir: Optional directory to save diff images
            pattern: Glob pattern for matching files (default: "*.png")

        Returns:
            Dictionary with comparison results for each file
        """
        dir1 = Path(dir1)
        dir2 = Path(dir2)
        results = {}

        if diff_output_dir:
            diff_output_dir = Path(diff_output_dir)
            diff_output_dir.mkdir(parents=True, exist_ok=True)

        # Find all matching files in first directory
        for img1_path in sorted(dir1.glob(pattern)):
            img2_path = dir2 / img1_path.name

            if not img2_path.exists():
                results[img1_path.name] = {
                    "status": "missing_in_dir2",
                    "error": f"File not found in {dir2}",
                }
                continue

            try:
                diff_path = None
                if diff_output_dir:
                    diff_path = diff_output_dir / f"diff_{img1_path.name}"

                mismatch, total, percentage, match = self.compare(img1_path, img2_path, diff_path)

                results[img1_path.name] = {
                    "status": "identical" if match else "different",
                    "diff_pixels": mismatch,
                    "total_pixels": total,
                    "diff_percentage": round(percentage, 2),
                    "diff_image": str(diff_path) if diff_path else None,
                }
            except Exception as e:
                results[img1_path.name] = {
                    "status": "error",
                    "error": str(e),
                }

        return results


def main():
    """CLI interface for image diffing."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Compare images and generate visual diffs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Compare two images
  python image_diff.py old.png new.png

  # Compare with diff output
  python image_diff.py old.png new.png --output diff.png

  # Compare directories
  python image_diff.py screenshots/old/ screenshots/new/ --dir-mode --output-dir diffs/

  # Custom threshold (more sensitive)
  python image_diff.py old.png new.png --threshold 0.05

  # Ignore anti-aliasing differences
  python image_diff.py old.png new.png --no-aa
        """,
    )

    parser.add_argument("input1", help="First image or directory")
    parser.add_argument("input2", help="Second image or directory")
    parser.add_argument("-o", "--output", help="Output path for diff image (file mode only)")
    parser.add_argument(
        "--output-dir", help="Output directory for diff images (directory mode only)"
    )
    parser.add_argument(
        "--dir-mode",
        action="store_true",
        help="Compare all images in two directories",
    )
    parser.add_argument(
        "-t",
        "--threshold",
        type=float,
        default=0.1,
        help="Matching threshold 0-1 (default: 0.1)",
    )
    parser.add_argument(
        "--no-aa",
        action="store_true",
        help="Ignore anti-aliasing differences",
    )
    parser.add_argument(
        "--pattern",
        default="*.png",
        help="File pattern for directory mode (default: *.png)",
    )

    args = parser.parse_args()

    # Create differ instance
    differ = ImageDiffer(
        threshold=args.threshold,
        include_anti_aliasing=not args.no_aa,
    )

    try:
        if args.dir_mode:
            # Directory comparison mode
            results = differ.compare_directory(
                args.input1,
                args.input2,
                args.output_dir,
                args.pattern,
            )

            # Print results
            print(f"\n📊 Comparing directories: {args.input1} vs {args.input2}")
            print(f"Pattern: {args.pattern}")
            print(f"Threshold: {args.threshold}\n")

            identical = []
            different = []
            errors = []

            for filename, result in results.items():
                status = result["status"]

                if status == "identical":
                    identical.append(filename)
                    print(f"✅ {filename}: Identical")
                elif status == "different":
                    different.append(filename)
                    diff_pct = result["diff_percentage"]
                    diff_pixels = result["diff_pixels"]
                    print(f"🔄 {filename}: {diff_pct:.2f}% different ({diff_pixels:,} pixels)")
                    if result.get("diff_image"):
                        print(f"   Diff saved: {result['diff_image']}")
                else:
                    errors.append(filename)
                    print(f"❌ {filename}: {result.get('error', 'Unknown error')}")

            # Summary
            print(f"\n{'=' * 60}")
            print("Summary:")
            print(f"  Identical: {len(identical)}")
            print(f"  Different: {len(different)}")
            print(f"  Errors: {len(errors)}")

            # Exit code based on differences
            sys.exit(0 if len(different) == 0 and len(errors) == 0 else 1)

        else:
            # Single file comparison mode
            mismatch, total, percentage, match = differ.compare(
                args.input1,
                args.input2,
                args.output,
            )

            # Print results
            print("\n📊 Comparing images:")
            print(f"  Image 1: {args.input1}")
            print(f"  Image 2: {args.input2}")
            print(f"  Threshold: {args.threshold}")
            print()

            if match:
                print("✅ Images are identical!")
            else:
                print("🔄 Images are different!")
                print(f"  Different pixels: {mismatch:,} / {total:,}")
                print(f"  Difference: {percentage:.2f}%")

            if args.output:
                print(f"\n💾 Diff image saved: {args.output}")

            # Exit code: 0 if identical, 1 if different
            sys.exit(0 if match else 1)

    except FileNotFoundError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"❌ Unexpected error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()
