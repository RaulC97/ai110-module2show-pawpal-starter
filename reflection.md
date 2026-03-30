# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    - To start, there is an Owner, Pet, Task, and Schedule.
- What classes did you include, and what responsibilities did you assign to each?
    - Owner has 1 or many Pets, Owner creates 0 or many Task, app creates Schedule.

**b. Design changes**

- Did your design change during implementation?
    - Yes
- If yes, describe at least one change and why you made it.
    - Changed the priority to an Enum instead of str, and use Date instead of str.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    - First its based on time, then theres a tie breaker check for priority
- How did you decide which constraints mattered most?
    - Time do to being a scheduling app, next was priority.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    - In the get_conflicts function in scheduler, i decided to make it more readable
- Why is that tradeoff reasonable for this scenario?
    - uses a defaultdict instead of a dictionary

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - Mostly for debugging and refactoring
- What kinds of prompts or questions were most helpful?
    - Mostly asking how to better fit the problem I was having

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - When creating the tests, there were some I didnt understand how it was going to test it properly.
- How did you evaluate or verify what the AI suggested?
    - Instead of accepting it, i had it explain what it was intending for the test.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    - Owner methods, scheduling algorithms and how it prioritizes sorting.
- Why were these tests important?
    - Made sure our classes were working properly, and if we make changes in the future, we use the test to make sure nothing affect the tests.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    - 4 out of 5
- What edge cases would you test next if you had more time?


---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - how the overall design feels

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - Improve on the look in streamlit

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - how AI tools are very good at seeing the big picture at the begining of a project and giving ideas on what to do, but when implementing more
    detailed task, like time conflicts, it may go overboard on thinking how to solve.
