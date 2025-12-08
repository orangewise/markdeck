# Mermaid Diagram Test

Testing mermaid diagram support in MarkDeck

---

## Flowchart Example

```mermaid
graph TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Great!]
    B -->|No| D[Debug]
    D --> B
    C --> E[End]
```

---

## Sequence Diagram

```mermaid
sequenceDiagram
    participant User
    participant Browser
    participant Server
    User->>Browser: Open presentation
    Browser->>Server: Request slides
    Server-->>Browser: Return slides
    Browser->>Browser: Render markdown
    Browser->>Browser: Render mermaid
    Browser-->>User: Display presentation
```

---

## Class Diagram

```mermaid
classDiagram
    class SlideShow {
        +slides[]
        +currentSlideIndex
        +init()
        +showSlide()
        +nextSlide()
    }
    class Slide {
        +content
        +notes
    }
    SlideShow --> Slide
```

---

## Git Graph

```mermaid
gitGraph
    commit
    commit
    branch develop
    checkout develop
    commit
    commit
    checkout main
    merge develop
    commit
```

---

## Pie Chart

```mermaid
pie title Language Distribution
    "JavaScript" : 45
    "Python" : 30
    "HTML/CSS" : 15
    "Other" : 10
```

---

## State Diagram

```mermaid
stateDiagram-v2
    [*] --> Loading
    Loading --> Loaded
    Loaded --> Presenting
    Presenting --> Presenting: Next/Previous
    Presenting --> [*]
```

---

# Success!

If you can see all the diagrams above, mermaid support is working correctly! 🎉
