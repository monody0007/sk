# Sekai's Memory System

What makes Sekai's memory system unique is its multi-character complexity. Traditional chatbots like ChatGPT typically manage one-on-one conversations, remembering only user facts and interactions. Open-source repositories like mem0 attempt to replicate this basic functionality.

Sekai's system is more sophisticated due to its multi-character nature, involving three distinct types of memory relationships:

1. **Character-to-User Memory**: Each character maintains separate memories with the same user. Character 1, Character 2, and Character 3 all develop unique memory relationships with the user character.  
2. **Inter-Character Memory**: Characters remember interactions with each other, creating an interconnected web of memories. Character A has memories with Character B, Character A with Character C, Character B with Character C, and so on.  
3. **World Memory**: Characters retain memories about the world's evolving state. For example, if Chapter 1 depicts a normal world, Chapter 10 introduces a zombie outbreak, and Chapter 20 shows Earth's destruction, each character develops different memories in response to these environmental changes.

This multilayered memory architecture creates significant complexity compared to traditional single-character chatbots, requiring a more sophisticated approach to memory management.

## **Project Overview**

Design and implement a memory system for a narrative-based application with multiple characters.

## **Requirements**

1. **Memory Database**  
   * Create a structure to store three types of memories:  
     * Character-to-User (C2U)  
     * Inter-Character (IC)  
     * World Memory (WM)  
2. **Core Functions**  
   * Write new memories  
   * Update existing memories  
   * Retrieve memories based on context  
3. **Evaluation Pipeline**

After you have built the memory system in **Part 1**, create an *automated* evaluation that answers three questions:

| \# | Question | Why it matters |
| ----- | ----- | ----- |
| **A** | *Does the system retrieve the **right** memories?* | Precision / recall of stored facts. |
| **B** | *Are the memories internally **consistent** across time, characters, and world state?* | Detects “cross‑talk” or forgotten updates. |
| **C** | Other evaluation rubric that you thinks necessary |  |

Feel free to explore LLM-as-judge, synthetic users, or any other paradigm that fits.

Bonus point: Make it an **online** eval pipeline that is able to analyze production data and detect issues near real time.

## **Data**

You'll work with a JSON file containing chapter data with synopses and memory information.

[https://drive.google.com/file/d/1A2XhTBCStFzYSwj28VGo\_9EuPzJgrTln/view](https://drive.google.com/file/d/1A2XhTBCStFzYSwj28VGo_9EuPzJgrTln/view)

## **Deliverables**

* Memory system architecture design and runnable prototype  
* A clear README on how to set up  
* A final report or observable dashboard demonstrating how the memory store change along with chat insertion.

## **Rubrics**

* **Completion** – All three deliverables are present and functional.  
* **Code Quality** – Readability, modularity, scalability, error handling, and clear documentation.  
* **Performance** – Low read/write latency, cost‑efficient token usage, and prudent vector‑store spending.  
* **Innovation** – Extra credit for creative features or insights beyond the core requirements, including those utilizing new AI frameworks.

