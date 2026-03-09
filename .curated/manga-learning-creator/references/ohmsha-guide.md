# Ohmsha Manga Guide Style

Guidelines for `--style ohmsha` educational manga comics.

## Character Setup

| Role | Default | Traits |
|------|---------|--------|
| Student (Role A) | 澶ч泟 | Confused, asks basic but crucial questions, represents reader |
| Mentor (Role B) | 鍝嗗暒A姊?| Knowledgeable, patient, uses gadgets as technical metaphors |
| Antagonist (Role C, optional) | 鑳栬檸 | Represents misunderstanding, or "noise" in the data |

Custom characters: `--characters "Student:灏忔槑,Mentor:鏁欐巿,Antagonist:Bug鎬?`

## Character Reference Sheet Style

For Ohmsha style, use manga/anime style with:
- Exaggerated expressions for educational clarity
- Simple, distinctive silhouettes
- Bright, saturated color palettes
- Chibi/SD (super-deformed) variants for comedic reactions

## Outline Spec Block

Every ohmsha outline must start with:

```markdown
銆愭极鐢昏鏍煎崟銆?
- Language: [Same as input content]
- Style: Ohmsha (Manga Guide), Full Color
- Layout: Vertical Scrolling Comic (绔栫増鏉℃极)
- Characters: [List character names and roles]
- Character Reference: characters/characters.png
- Page Limit: 鈮?0 pages
```

## Visual Metaphor Rules (Critical)

**NEVER** create "talking heads" panels. Every technical concept must become:

1. **A tangible gadget/prop** - Something characters can hold, use, demonstrate
2. **An action scene** - Characters doing something that illustrates the concept
3. **A visual environment** - Stepping into a metaphorical space

### Examples

| Concept | Bad (Talking Heads) | Good (Visual Metaphor) |
|---------|---------------------|------------------------|
| Word embeddings | Characters discussing vectors | 鍝嗗暒A姊︽嬁鍑?璇嶅悜閲忓帇缂╂満"锛屾妸涔︽湰鍘嬬缉鎴愬僵鑹插皬鐞?|
| Gradient descent | Explaining math formula | 澶ч泟鍦ㄥ北璋峰湴褰笂婊氱悆锛屽鎵炬渶浣庣偣 |
| Neural network | Diagram on whiteboard | 瑙掕壊璧拌繘鐢卞彂鍏夎妭鐐圭粍鎴愮殑缃戠粶杩峰 |

## Page Title Convention

Avoid AI-style "Title: Subtitle" format. Use narrative descriptions:

- 鉂?"Page 3: Introduction to Neural Networks"
- 鉁?"Page 3: 澶ч泟琚捣閲忓崟璇嶆饭娌★紝鍝嗗暒A姊︽嬁鍑?璇嶅悜閲忓帇缂╂満'"

## Ending Requirements

- NO generic endings ("What will you choose?", "Thanks for reading")
- End with: Technical summary moment OR character achieving a small goal
- Final panel: Sense of accomplishment, not open-ended question

### Good Endings

- Student successfully applies learned concept
- Visual callback to opening problem, now solved
- Mentor gives summary while student demonstrates understanding

### Bad Endings

- "What do you think?" open questions
- "Thanks for reading this tutorial"
- Cliffhanger without resolution

## Layout Preference

Ohmsha style typically uses:
- `webtoon` (vertical scrolling) - Primary choice
- `dense` - For information-heavy sections
- `mixed` - For varied pacing

Avoid `cinematic` and `splash` for educational content.
