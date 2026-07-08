# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
    - I have an Owner, Pet, Task and Scheduler class. The owner class can have 1 or more pets. Pets can have 1 or more tasks. A scheduler can manage 1 or more classes.
- What classes did you include, and what responsibilities did you assign to each?
    - Owner class: contains information on the pet Owner. lists all pets owned. Can add and remove pets and update contact information
    - Pet class: has information (id, name, species, breed, age, owner, tasks). Can add/remove/list tasks and update info
    - Task class: (id, title, type, due date, recurring) mark task as complete/incomplete. checks if it is overdue and can reschedule
    -


**b. Design changes**

- Did your design change during implementation?
    - Yes
- If yes, describe at least one change and why you made it.
    - I added support for data sync between pet and owner, that way changes made to either class wouldn't have errors in copying over

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
    - I chose a time slot constraint to show if there are any clashing task. There is a filter constraint for the completion status.
- How did you decide which constraints mattered most?
    - I used the constraints that were already given in the data, due date, time, completed and recurrence.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
    -  There is no checking for task overlap, only if they start at the same time.
- Why is that tradeoff reasonable for this scenario?
    - Petpal works more as a remainder app, ensuring the owner is able to see what they need to do.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
    - I used my AI coding assistant to implement each scheduling feature (sorting, filtering, recurrence, conflict detection) on top of the class skeletons, to draft the pytest test suite, and to keep the README and UML in sync with the final code.
- What kinds of prompts or questions were most helpful?
    - Narrow, single-feature prompts worked best ("add sort_by_time using sorted() with a lambda on the HH:MM string"). Asking it to *explain* a choice — e.g. why `timedelta` handles month rollover — was more useful than asking it to just write code, because it let me confirm the logic before saving.

**b. AI strategy**

- Which AI coding assistant features were most effective for building your scheduler?
    - Editing multiple files in one step (e.g. adding the `time` field to `Task` *and* the `sort_by_time`/`filter_tasks` methods in `Scheduler` *and* wiring them into `main.py`) kept the layers consistent. Running the demo and the pytest suite in the terminal and reading the output back was the biggest confidence-builder — I could see green checkmarks instead of trusting the code blindly.
- Give one example of an AI suggestion you rejected or modified to keep your system design clean.
    - The assistant first proposed a stateful task-ID counter stored on the `Scheduler`. I rejected it because it would have to stay in sync with the counters already living in `app.py`'s `st.session_state`. I had it switch to deriving the next ID from `max(existing task_id) + 1` (`_next_task_id()`), so recurrence spawning has no hidden state to drift.
- How did using separate chat sessions for different phases help you stay organized?
    - Keeping one session per phase (logic → tests → UI/docs) meant each conversation carried only the context it needed. When debugging a failing test I wasn't wading through UI discussion, and when polishing the README the assistant already "knew" the finished method names from that phase's context.

**c. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
    - See the task-ID counter above. I also tightened the conflict warning so it lists the clashing pet names, not just a count, because a bare "2 tasks clash" isn't actionable for an owner.
- How did you evaluate or verify what the AI suggested?
    - I ran `python main.py` to eyeball behavior and `python -m pytest` to check correctness against explicit assertions. A suggestion only got saved once the demo output and the tests both agreed with what I expected.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
    - Task basics (mark_done, add_task), sorting correctness (out-of-order tasks come back chronological), recurrence (completing a daily task creates a next-day task on the same pet), and conflict detection (duplicate time slots flagged, distinct times produce no false positive). Six tests total, all passing.
- Why were these tests important?
    - They cover the "smart" logic that a pet owner actually relies on. Sorting and conflict detection are the features most likely to break silently — a wrong sort or a missed clash looks fine on screen but gives bad advice — so pinning them with assertions matters most.

**b. Confidence**

- How confident are you that your scheduler works correctly?
    - Fairly confident (4/5). The core paths are green in pytest and match the demo output, but coverage isn't exhaustive.
- What edge cases would you test next if you had more time?
    - Weekly recurrence math, month/year date rollover (e.g. Jan 31 + 1 day), an empty scheduler, tasks with no pet back-reference, and the Streamlit UI wiring in `app.py` (which pytest doesn't touch).

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
    - The clean separation between the logic layer (`pawpal_system.py`) and the UI (`app.py`). Because every "smart" behavior lives in a `Scheduler` method, the UI just calls them and the same methods are covered by tests — no logic duplicated in the front end.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
    - I'd add task duration so conflict detection catches real overlaps, not just identical start times, and add a priority field so the schedule can rank tasks instead of only sorting by clock time.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
    - Being the "lead architect" means the AI writes code fast, but I own the design decisions. The assistant's first answer is a draft, not a verdict — my job was to keep the boundaries clean (reject the stateful counter, keep logic out of the UI), verify every suggestion with the demo and the test suite, and only then accept it. AI accelerates the typing; the judgment about what makes a coherent system stays with me.
