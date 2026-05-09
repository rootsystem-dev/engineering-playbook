# Vibe Engineering: A Field Manual
for AI Coding in T eams
How to build reliable, scalable workflows for agent-assisted coding
without risking your repo or business.
Alex Chesser Following 32 min read · Aug 5, 2025
--- 
57 7
LLMs have become our co-workers, it’s time to learn how to work together. (Image credit: ChatGPT)
## The T wo-Minute Debrief:
### For Leaders
Lasting advantage comes from redesigning core workflows, not just
adding tools. The highest-performing AI adopters see up to 6x higher
shareholder returns by making these structural changes. (McKinsey,
2024)
Recruiting, retaining, and promoting engineers who are mastering AI
tools and practices is arguably the single most impactful lever for early
success. Vibe Engineering provides the framework to amplify their
individual capabilities across the organization.
Effective sponsorship is not about AI mandates; it’s about providing
“immunosuppressants” to protect teams from the “corporate immune
system” as they experiment and manage the risk of failure.
The rush for velocity is a trap if it tanks your Change Failure Rate (a key
DORA metric). The goal is supervised speed, not reckless acceleration.
### For T echnologists
Stop “vibe coding”
. Start Vibe Engineering — a practice that treats
prompts as version-controlled architectural artifacts, not as disposable
hacks.
Unsupervised AI can make you slower (METR, 2025). Studies show it can
increase code churn and reduce overall development speed. (GitCear,
2023)
The Vibe Engineering lifecycle provides a structured recipe : use
Prework to set guardrails ,
Planning to version-control intent , and
Execution to generate code against a trusted plan.
A Field Manual for T wo Fronts
This article is designed for two distinct but related audiences. To get the
most value, find your path below.
For Strategists, Leaders, and Managers: Read from the top. The first half
(Sections 1–6) establishes the “why”: the strategic landscape, the data
behind high-performing AI teams, and the organizational dynamics that
separate leaders from laggards.
For Engineers, Architects, and Practitioners: Skim the first half for
context, then jump directly to the “how” in Section 7: The Vibe
Engineering Development Lifecycle. This is the hands-on recipe with
code, prompts, and repository structures you can implement
immediately.

# 1. The Call to Action: Mastering AI-Assisted Coding
AI-assisted coding is no longer a futuristic concept; it’s a daily reality in the
enterprise. Large Language Models have joined our teams, reshaping how
code is written, reviewed, and deployed. Yet, for many engineering
organizations, this powerful shift has brought more chaos than clarity.
Teams find themselves wrestling with a tangle of outdated workflows,
change-resistant processes, and a pervasive sense of “vibe coding”
— an
uncritical acceptance of AI output that risks stability for the illusion of
speed.
This isn’t just about adopting new tools; it’s about fundamentally redesigning
the way we work. While tech giants rapidly prototype autonomous code
generation, most companies are still searching for a scalable, reliable way to
integrate AI without risking their entire codebase. The promise of
unprecedented velocity often clashes with the harsh reality of increased
code churn and a higher Change Failure Rate. Reckless acceleration is a trap;
true advantage comes from supervised speed.
This Field Manual cuts through the noise. It offers a hands-on, battle-tested
recipe for introducing Vibe Engineering into your enterprise workflows.
Built from real-world examples and grounded in a philosophy that keeps
humans precisely in the loop — without slowing them down — this guide
provides the structured approach you need. We’ll show you how to transform
ad-hoc prompting into a disciplined practice, treating prompts as version-
controlled architectural artifacts, not disposable hacks.
It’s time to move beyond hoping for the best and start engineering for
success. Welcome to the future of collaborative coding.
# 2. The Pitfalls of Vibe Coding
At this point, it’s clear: vibe coding is having its hot girl summer.
The neologism burst into tech culture seemingly overnight — trending fast
since February. Broadly speaking, it refers to accepting whatever code your
LLM gives you, uncritically, and letting the statistical haze of a transformer
model guide your output. You vibe, it codes.
Vibe coding is the practice of working alongside a generative AI tool, often
without rigorous supervision or validation, and accepting its output as-is or
with minimal oversight. It emphasizes flow, speed, and exploration — but
often at the cost of accuracy or robustness.
For many seasoned engineers, this triggers a visceral reaction — ranging
from cautious curiosity to outright horror. We remember the time a missing
semicolon brought down production. We’ve lived the reality of complex
systems where safety margins are thin and even minor changes ripple in
unexpected ways.
It’s hard to imagine placing your trust in an AI agent that writes code based
on probabilities rather than principles.
Stories like this one — where an AI agent deleted a production database — or
this one, where a model apologized for catastrophic failure, do little to
reassure the skeptics. And yet… the speed. The speed is undeniable. It looks
like a magic trick. It feels unreal.
This rush to adopt generative tools reflects a deeper, industry-wide pursuit of
elite engineering performance. The canonical DORA metrics — Deployment
Frequency, Lead Time for Changes, Change Failure Rate, and Time to
Restore Service — have become the C-suite’s preferred scorecard for
developer productivity.

On the surface, AI-assisted coding promises to dramatically improve lead
time. The risk, however, is a corresponding explosion in the Change Failure
Rate. If velocity comes at the cost of stability, the net gain is zero. As leading-
edge thinkers like Nora Jones, a key voice in software reliability would argue,
any system that introduces this much probabilistic output must be treated as
an inherently unpredictable dependency.
It must be contained and validated, not blindly trusted.
Executives see that velocity and can’t help but imagine what their businesses
would look like if their entire development org moved at that pace. The
companies that learn to harness that speed safely — without losing control —
will have a profound competitive advantage.
This is the core tension: reckless acceleration versus cautious skepticism.
The future won’t be won by those who reject vibe coding outright, nor by
those who embrace it blindly. It will belong to the teams who build systems
to channel that speed — supervised, structured, and scalable.
At the top of the organization, in the C-suite and on the board, AI is no
longer a curiosity — it’s a mandate. Make no mistake: anyone who reports to
executive leadership in 2025 has an OKR that includes “find the AI play” by
next quarter.
A recent discussion thread —
“Forced AI nonsense hysteria happening at
your company?”
— has hundreds of comments from engineers and PMs
alike, all lamenting the leadership scramble to inject AI into anything with a
pulse. It’s like we’ve all been handed a very shiny hammer, and now we’re
desperately searching for something — anything — that looks like a nail.
# 3. The Unfulfilled Promise of Agentic Coding
Even as enterprises acknowledge the risks of “vibe coding,
” many have
rushed to implement “agentic coding” workflows, hoping for a swift path to
productivity gains.
Procurement departments are working overtime, securing tools and
licenses. Engineers are getting tools like Cursor or Claude Code in their
hands, and are being told: “Now go be faster.
”
Yet, they’re not getting a playbook and are having to figure out how on their
own. The guidance on how to integrate these powerful AI collaborators
effectively, without disrupting existing processes, is a missing link.
In the enterprise, where decades of process has worn grooves into the
carpet, the guidance is simple: keep doing everything the same — just do it
quicker. Use the same ceremonies, the same commits, the same signoffs.
Only now, it’s like you’ve got Stack Overflow pre-downloaded into your IDE.
The answers arrive instantly. They don’t yell at you for asking dumb
questions. Job done. You’re an AI-powered organization now. Time to go
home.
Step too far out of line, and the veneer of a generative culture — the kind
described in Accelerate as a hallmark of high-performing engineering teams
— starts to peel away. Instead of learning and adapting, teams revert to fear
and blame.
“You vibe coded this.
” It’s becoming a slur among the old-school artisans.
They’ll say the LLMs can’t match their level of rigor. But more than that, they
don’t trust that you even tried.
The results aren’t helping. Despite the promises of speed, early data is
mixed. In one study, Cursor-based development came in up to 19% slower
on average. Whatever agentic coding is supposed to be, it’s not delivering
consistent velocity gains.
However, interpreting these findings requires nuance: many participants
noted that while the AI was generating code, they would often context-switch
or browse other content, effectively waiting for the AI. This suggests that
“time to complete” metrics alone may not fully capture the efficiency gains,
as human-AI collaboration introduces new workflow dynamics where
engineers might choose to optimize for parallel activity rather than
continuous, synchronous coding.
A 2023 GitClear analysis of over 150 million lines of code suggested that
while AI assistance increases code volume, it can negatively impact code
quality and maintainability, leading to more churn and a higher percentage
of code being undone or modified shortly after being written. This aligns
with the anecdotal experience of many teams: the initial burst of speed is
often paid back, with interest, during code review and debugging cycles.
So, who is doing this right?
# 4. Who’s doing this right?
To understand what high-performance looks like, we cannot rely on a single
source of truth. The patterns of success are visible when we triangulate
findings from management consulting, internal research at hyperscalers,
and quantitative analysis of development lifecycles. While consulting reports
provide a high-level strategic view, data from Google’s internal developer
surveys and the DORA State of DevOps reports provide complementary,
ground-level validation.
Leading analyses suggest that a single largest driver of increased EBIT
among high-performing AI adopters is the redesign of core business
workflows using generative technologies. These aren’t marginal gains from
chatbots or customer-facing gimmicks — they’re structural improvements to
how work gets done internally.
While the precise causal link — whether these traits enable leadership or are
results of having greater resources — is open for debate, what is clear is that
these characteristics define organizations that are successfully leveraging AI.
The principles of Vibe Engineering are designed to help any team cultivate
these traits, regardless of their current position.
A related study, Rewired and Running Ahead, segmented companies into
digital “Leaders” and “Laggards.
” Across all sectors, Leaders saw 2x to 6x
higher total shareholder returns than their peers. More importantly, the
gains are compounding over time — the gap is widening.
So what are the leaders doing differently?
Common Traits of Generative AI Leaders:
They redesign workflows, not just tools Focus is placed on how work
flows across teams and systems — not just adding AI into the mix.
It sounds abstract, but in practice, this means treating the inputs to the LLM
as first-class engineering artifacts. The workflow is redesigned when the
source of truth for a task shifts from a brittle JIRA ticket to a version-
controlled prompt chain that lives next to the code. This isn’t a visionary
restructuring; it’s the pragmatic work of moving architectural context to
where it can be executed — at the keyboard, not in a steering committee.
They empower cross-functional teams Teams that combine domain
expertise, engineering, and design work together to implement AI across
use cases.
Agentic systems fail at the boundaries of specialized knowledge. An LLM
cannot infer a product manager’s unstated commercial goals or a
compliance officer’s regulatory constraints.
“Empowerment” is therefore a
defensive necessity. It means the domain experts who hold this critical
context are given direct agency over the prompts that guide the AI. This is
not about collaboration for its own sake; it is about injecting siloed human
knowledge into the workflow at the point of maximum leverage, preventing
context collapse before it occurs.
They build reusable platforms Leaders invest in shared prompt
repositories, fine-tuned models, and centralized policy enforcement —
not just distributed tools.
Leading organizations understand that a “platform” is not just about tools; it
is about creating a system of leverage. A shared, version-controlled
repository of prompts and architectural rules is the platform. Each
committed example and refined prompt is a unit of codified knowledge that
lowers the activation energy for the next developer. This approach attacks
the single greatest source of waste in AI-assisted coding: the thousands of
hours teams spend independently “prompt-flailing” to solve problems that
have already been solved by a colleague down the hall.
They treat AI as an operating model shift Generative AI is not a project.
It’s a shift in how value is created.
This is the distinction between adoption and transformation. Laggards treat
generative AI as a feature to be used; leaders integrate it as a fundamental
change to the physics of software production. The operating model has
shifted when “refine the prompt” becomes a standard ticketable task, when
“prompt quality” is a metric in code reviews, and when the act of generating
a development plan is itself a version-controlled artifact. The work is no
longer just building the “what”; it is also building the “how.
”
They have CEO-level sponsorship industry observations have found a
strong correlation between performance gains and whether the CEO
personally led the AI transformation effort.
In most companies, the corporate immune system attacks anything that
deviates from established process. CEO-level sponsorship is the prescription
for immunosuppressants. Its purpose is not to issue top-down commands,
but to protect the teams doing the messy, ground-level work of integration
from being ground down by procurement, compliance, and risk-averse
middle management. The true signal of sponsorship is not a keynote speech
or a memo; it is when a team’s experimental AI workflow fails and the post-
mortem is a blameless analysis of what to improve, not a search for who to
punish.
These organizations aren’t “vibing harder” or just stacking tools on top of
existing infrastructure. They are deliberately rewiring their workflows to
enable AI to augment high-leverage activities: coding, analysis, decision-
making, and customer design.
# 5. Why the Midmarket and Enterprise Lag Behind
For most midmarket firms and slower-moving enterprises, the problem isn’t
a lack of talent or ambition. It’s the operating context. Legacy systems run
deep. Decision rights are distributed. Procurement takes quarters. Risk
tolerance is low. Accountability frameworks reward predictability over
experimentation.
This resistance is not merely cultural; it is structural. In The Manager’s Path,
Camille Fournier describes the immense coordination overhead required to
enact technical change in established organizations. Introducing a
technology as foundational as an AI coding partner isn’t a tooling decision —
it’s a systems architecture decision with deep implications for team
structure, cognitive load, and accountability. Without a clear mandate and a
strategy for managing this complexity, a bottom-up adoption of agentic
coding will invariably collide with the organization’s immune system.
Experienced engineers have seen this movie before. We know the hype
cycle. We know how bad things can get, like the time 11 lines of javascript
shut down deployments for about half the internet. Resisting hype is a core
function of the enterprise engineer’s job.
We’re allowed to get excited by shiny new tools on our own time. But on the
job, we’re stewards of complexity. At work we have a job to do and in some
cases there are millions of dollars and the well being of thousands of
humans on the line.
When the product is already working, tossing it into the jaws of a language
model sounds less like vision and more like malpractice. A stable production
environment means everyone, including them, gets to go home at the end of
the day and walk the dog, hug their kids, and get a great night’s sleep.
The 12 Practices of AI Transformation
Reimagine workflows
Prioritize use cases by value and feasibility
Build cross-functional AI teams
Invest in reusable AI components
Create data products with ownership
Build scalable MLOps and LLMOps pipelines
Launch an AI governance framework
Educate and empower business users
Track adoption and value realized
Redesign org structure to support AI scale
Embed AI into performance management
Ensure CEO-level sponsorship
Any one of the best practices is non-trivial. Taken together, they represent an
organizational shift that touches almost every function. It’s uncomfortable
work. And without leadership authority and sustained focus, it rarely holds.
Shifting the working model of teams isn’t something that can plausibly be
driven from the bottom up. In practice, it requires time, trust, and top-down
air cover.
In Turn the Ship Around, David Marquet argues that great organizations shift
from a leader–follower model to a leader–leader model. Authority is
redistributed, not abandoned. This doesn’t mean chaos — it means clarity,
intent, and shared ownership.
Marquet’s intent-based leadership model provides the command-and-control
framework, but Google’s internal research on psychological safety provides
the execution-level insight. For developers to effectively adopt, critique, and
refine AI-generated outputs, they must feel safe to experiment and, crucially,
to report failures without blame. When a developer can say,
“The agent
hallucinated a deprecated library and I spent half a day debugging it,
” and
the response is “Good catch, let’s update the prompt template for the team,
”
that is the moment a generative culture becomes real.
The transformation works when teams are trusted to act, and equipped to
succeed.
# 6. It’s Time for Vibe Engineering
If the earlier sections of this piece sounded cautious, it’s because caution is
justified. Most organizations have good reasons to hesitate. But eventually,
the cost of doing nothing starts to exceed the risk of doing something. That’s
where we are now. It’s time to try something new — on purpose, and with
intent.
Let’s give that intent a name: Vibe Engineering.
This paradigm shift isn’t just about technical proficiency; it’s about a
fundamental redefinition of roles and responsibilities. Drawing from Peter
Drucker’s insights over half a century ago in The Effective Executive, effective
leadership focuses not on making all the right decisions themselves, but on
equipping knowledge workers with the information needed to make sound
decisions.
In the era of AI-assisted coding, developers are increasingly taking on an
executive function themselves, not for human knowledge workers, but for
their burgeoning AI collaborators.
Our greatest challenge, and indeed our greatest opportunity, now lies in
diligently curating and communicating the precise “information” that our
LLMs need to function as truly effective, non-hallucinating partners.
Some might argue that as AI advances, such structured approaches become
brittle, or that “prompt tricks” will soon be irrelevant. Indeed, AI capabilities
are evolving at an astonishing pace, and models are increasingly capable of
inferring intent. However, the core philosophy of Vibe Engineering
transcends mere prompt engineering; it’s about engineering the interface
between human intent and AI execution.
Even with more capable agents, the need to version control collective
knowledge, ensure reproducibility, and establish guardrails for complex
systems remains. As AI becomes more powerful, the emphasis shifts from
micro-prompting to macro-orchestration, where understanding and managing
the intent behind the code, and ensuring its alignment with business logic,
becomes even more paramount.
Vibe Engineering provides a resilient framework for this ongoing evolution,
ensuring that as AI grows more capable, our ability to direct and integrate its
power scales responsibly.
This means treating every prompt, every piece of context, and every rule as a
vital, version-controlled asset — the “information” that fuels the AI’s “right
decisions.
” It’s about ensuring that documentation is not just an
afterthought, but actively baked into the prompt engineering workflow. This
approach echoes the ethos of leading engineering organizations, where
documentation, when treated as a first-class citizen, is recognized as one of
the most infinitely scalable technologies an organization can introduce.
This discipline transforms coding tools into true teammates, fundamentally
shifting how we engage with prompts: We stop treating prompts like one-off
hacks, and start treating them like architecture. Inputs, patterns, examples,
and responses — all shaped into something cohesive, repeatable, and
improvable.
This resilience is further amplified by the human element. By enabling your
most experienced “10x AI-enabled engineers” to codify their intuition and
best practices into version-controlled prompts, Vibe Engineering effectively
democratizes their expertise. This means that highly complex tasks,
previously restricted to a few experts, can now be executed by a broader
range of team members with confidence, allowing the entire organization to
“level up” its AI capability and achieve supervised speed at scale.
We’re no longer lone wolves, vibe coding into the void. This is pack work
now.
One prompt isn’t a strategy. But when we start linking them — adding
context, examples, team-wide conventions — we’re building the
infrastructure that unleashes velocity.
We’re moving beyond fast typing into a coordinated system design:
communication, framing, and iteration as real engineering artifacts.
Vibe Engineering emphasizes living context — prompts, conversations,
embedded examples, and iterative demonstrations that evolve alongside the
code. And like code, they belong in version control. As the authors of
Software Engineering at Google put it “Documentation must be as close to the
code as possible. It must be easy to maintain, easy to keep up to date, and easy to
find.
”
The same rule applies to the artifacts of prompt work. If we want reusable,
composable agent behavior, we have to treat the inputs like first-class
citizens.
This is why we don’t bury prompts in ticketing tools. It’s why we store them
alongside the code they’re meant to support. Tools like Cursor run on disk.
The closer the input lives to the implementation, the faster iteration
becomes. And speed of iteration is the compound interest of Vibe
engineering.
Each time a prompt example gets checked in — each time someone stops to
show “what good looks like”
— we increase the reliability of future work. We
reduce prompt flailing. We transfer know-how. We build muscle. Over time,
the planning phase shortens, and the execution tightens. The more you
commit to this practice, the more leverage you create.
This is what happens when you treat communication like code — everything
gets sharper. In this way, the codebase becomes not just a record of what was
built — but of how we learned to build it better.
7 . The Vibe Engineering Development Lifecycle
We’ve established the case for treating prompts as reliable, living artifacts.
Now, let’s get specific. This section details the Vibe Engineering
Development Lifecycle, a structured approach to integrating AI into your
team’s coding workflows. Through a set of practical examples — synthesized
from real-world agent collaboration patterns — we’ll demonstrate how
prompting can become a first-class discipline in your team.
These examples are bespoke and hand-crafted exclusively for this article in
order to illustrate principles, tradeoffs, and the kinds of artifacts that can
move the needle for enterprise teams. There is no proprietary work from
any other repository contained within. Use them as inspiration, not gospel —
tune or critique as your own context demands.
An overview of the Vibe Engineering Development Lifecycle
The Vibe Engineering Development Lifecycle follows a high-level workflow
broken down into three crucial stages: Prework, Planning, and Execution.
First, in Prework, teams interrogate architecture and draft guiding rules to
establish essential guardrails.
Next, the Planning phase involves drafting and iterating on prompts that will
orchestrate precise code generation.
Finally, Execution uses those refined prompts to generate and review code
segments, iterating until the solution is ready for deployment.
Loops within Planning and Execution ensure continuous refinement and
improvement, reflecting our core thesis of prompts as evolving, living
artifacts.
In the following subsections, we’ll explore each phase in detail, starting with
Prework, then Planning, and finally Execution — complete with concrete
prompt examples and workflow practices you can adapt for your team.
## 7 . 1 Prework: Preparing the Repository
The Prework Phase is about crafting a set of guardrails unique to your
codebase. This grounds prompt-driven generation in your team’s unique
architecture and standards — key for avoiding hallucinations and ensuring
the AI acts within meaningful guardrails.
To begin, create a folder at the root level of your Git repository: .development-
context/research.
Now, create a file within that folder called 01-architectural-research-
prompt.md. This file will contain the instructions for your AI agent to analyze
your repository and generate an architectural research document.
Note on formatting: prompt line length has been optimized for printing on
medium. This was a decision to benefit readers of this article and does not need to
be replicated in your codebase.
Create a document 02-architectural-research.md
which details the tools, frameworks and design
patterns used across the repository.
Pay particular attention to highlight any
standards and practices that appear to deviate
from those that one would expect to find given
the recommended advice of the language and
framework.
The description should include but not be
limited to highlighting data models, api
design & versioning, as well as any other
insights that seem relevant within the
current state of the repository.
(for legacy systems)
When more than one or conflicting architecture
or pattern is being used, call this out in the
document and provide recommendations on the
best direction forward. Use references to
external sources which can qualify known best
practices from software experts.
When it is clear when there is an old or a new
way of doing things, call out which one is the
newer pattern.
Next, inside your agent, use this prompt to execute the instructions you’ve
just created:
Execute the instructions found within
@01-architectural-research-prompt.md
Now, carefully read the artifact that was produced ( 02-architectural-
research.md). Does it seem accurate? Are there things you think you should
correct? Some inaccuracies (‘hallucinations’) are expected in early iterations
and can be corrected through iterative prompt refinement. For simple
errors, feel free to edit them manually.
For things that appear to be more systemic or outright mind-blowingly
wrong, don’t panic.Go back and edit the 01-architectural-research-prompt.md
to include additional context or directives it shouldn’t forget. Focus on
capturing the most significant errors for targeted prompt improvements
rather than exhaustive corrections. We’re building these systems for the long
haul and expect to to be iteratively improving them for years to come. It is a
mistake at this point to sacrifice velocity in favor of perfection. Simple errors
can and should be manually corrected, keeping the focus on meaningful
prompt refinement over exhaustive fixes.
You’re going to keep both of these documents ( 01-architectural-research-
prompt.md and 02-architectural-research.md) and check them into your
repository. They form the foundation of your architectural context.
We’re not quite ready to get rolling on an actual project yet. Your next step is
to execute another agentic command to codify these insights into reusable
rules:
Read @02-architectural-research.md and create
a series of cursor rules using their
documentation
https://docs.cursor.com/en/context/rules#rules
Save each in a separate file in the folder
.development-context/rules and include a
readme.md document which describes each
rule and explains when it is appropriate
to use them.
For example, planning a task without data
migrations would not need to include any
database rules. But if it were modifying
an endpoint it might be appropriate to
include api design rules.
Review those rules carefully and check them into your repository after you
agree with all of them. Now, you’re ready to proceed to the Planning phase.
## 7 .2 Planning
The Planning Workflow
With architectural context and rules in place, the next phase is where
strategy meets code: Planning.
Here, agentic prompting becomes a first-class part of your engineering
workflow — writing, reviewing, and refining prompts that translate high-
level tickets into actionable, review-ready development plans. The goal isn’t
just to produce a plausible “to-do” list, but to create durable, versioned
planning prompts that reflect your team’s evolving standards and
knowledge.
In this section, you’ll learn how to:
Capture your team’s implicit habits and know-how as explicit, reviewable
agent instructions.
Structure prompts that produce plans worth reviewing — moving beyond
“good enough to start coding.
”
Apply practical review loops and lightweight iteration to evolve rough
plans into confident, team-aligned artifacts.
https://alexchesser.medium.com/vibe-engineering-a-field-manual-for-ai-coding-in-teams-4289be923a14#11-references-and-further-reading 13/24
8/19/25, 11:54 AM Vibe Engineering: A Field Manual for AI Coding in Teams | by Alex Chesser | Aug, 2025 | Medium
Planning is the inflection point where ad hoc prompting becomes a
managed, improvable practice — the beating heart of Vibe Engineering.
### Step 1: Set Up Y our Planning Context
Repository structure:
Within .development-context , create a new folder named for your
{ticket-id}
Save a text copy of the requirements into 01-product-requirements.txt
Create 02-initial-planning-prompt.md with a prompt template such as:
Draft a delivery plan for
@01-product-requirements.txt. Include context
from .development-context/rules per
@.development-context/rules/readme.md.
Break the work into small, logical units
(use trunk-based development).
Ensure the plan specifies a series of
individual pull requests.
We will be sending out code into a live,
working production application that is
business critical safety is paramount.
Each step in the plan should include a
justification for why it is safe to
deploy to production.
If appropriate, use feature flags or ensure
deployed code isn't executed until enabled
later.
Organize parallelizable work into tracks.
Optimize the plan for "the three reads of
design":
Start with a high-level executive summary.
Next, a bullet-point ToC of phases, tracks,
and PRs (with descriptions, anchor links).
At the highest level, this should be suitable
for someone to be able to hold the whole
project in their head. One or two sentences
at most.
Finally, detailed instructions per PR:
highlight the specific files, objects,
and paths to be touched (use code formatting).
Don't include large code samples, when the PRs
come along the code will be there and we want
to eliminate redundancy for the humans doing
the planning right now and code reviewers
later.
DO specify method signatures or API contracts.
Using "API first" development philosophy
guidance as found within the "15-factor-app"
paper on development best practices.
Write your output to [02-initial-plan.md] in
the same folder.
#### Tip:
Any reusable portion of this prompt (excluding the live requirements)
belongs in a shared prompt artifact, e.g. planning-starter-prompt.md that
lives in your rules folder
This makes process and standards consistent — letting anyone, from interns
to lead architects, leverage your best patterns in planning. This effectively
codifies the tacit knowledge of your most experienced talent, making their
hard-won insights actionable for the entire organization.
### Step 2: Run the Agent, Review, and Stage
Run the prompt by instructing your agent:
Using @02-initial-planning-prompt.md generate
l f @01 d t i t t t
#### Tip:
Stage but don’t commit the plan immediately. Staging in git creates a “safety
checkpoint”: any edits remain visible in the diff, making it easy to review
what’s changed and why, before you solidify your copy.
### Step 3: Iterative Review (The “Three Reads”)
Early AI-generated plans will rarely be perfect — and that’s OK. Expect to
iterate:
First read: Executive Summary.
Did the LLM grasp the main point and success criteria? Would you share
this with your manager?
Second read: Table of Contents.
Do titles match architecture and expected tracks? Watch for fundamental
misunderstandings (e.g., proposing manually writing code systems that
are autogenerated). Don’t hesitate to remove unnecessary work.
Third read: PR Details.
Are the right files being changed? Is the scope safe and reviewable?
Double-check success criteria and merge-safety justifications. Compare
the plan to actual ticket requirements, not just what you pasted in
initially.
Pro tip: Unwanted artifacts are normal. Use iterative, conversational edits
(“Ignore observability — we use auto-instrumentation”; “Don’t estimate
timings — they’re unreliable”) to guide the agent. Over time, roll recurring
lessons into your planning-starter prompt.
### Step 4: Socialize and Secure T eam Buy-In
Once it passes your review, check the plan into the repo in its own
branch (not yet a merge request). This makes the plan visible, reviewable,
and optimized for summary or deep-dive by teammates and product
owners.
Invite local experts — and product partners, if valuable — to pressure test
the plan. Use their feedback to further refine your prompt or outputs.
The first and second reads in a typical project should not take up more
than a page of text. This is a fantastic time to involve more senior
members of your team and less technical members. Let’s gather rock-
solid alignment on what we’re building here.
The third read is where it gets really gritty, this is where we’d typically see
the group whittled down to just the engineers and a key front line
Product Manager.
### Step 5: T each your prompt what good work looks like.
Leverage approved plans as ‘gold standards’: Once a plan has been
collaboratively reviewed and refined, use its final content to further
improve your prompts.
Close the feedback loop: Actively incorporate these real-world, approved
examples back into your original planning prompt (or a dedicated
example file referenced by it).
Build ‘living context’: This teaches your AI what successful outputs look
like, significantly reducing the need for manual fine-tuning and ‘prompt
flailing’ in subsequent runs.
Tighten the iteration cycle: You’ll be amazed at how much less fine-
tuning you need the next time you generate a plan.
// ... paste this immedaitely after
// the third read.
<example>
[paste an example of one of the
PR-plans that your team eventually
approved, the precise content here
isn’t as important as the final
format, including the sections and
headings that you settled on]
</example>
Tip:
This is also an excellent time to take this prompt and move it into a file
under rules called planning-starter-prompt.md. That way, the next time you
come at planning, the quality of your first pass is much better.
Key T akeaways
Each planning prompt becomes a living artifact — versioned,
reviewable, and improvable.
Staging and iterative review encourage confidence without bureaucracy.
Artifacts can be reused and evolved: Your best practices scale to all
engineers, amplifying institutional memory and decision quality.
When the team is aligned and the plan is set, you’re primed to move into
execution with clarity and confidence.
## 7 .3 Execution: T urning Plans into Code
Begin with the prompt, sent directly to your agent:
Execute Track 1 PR 1 in
@/{tickt-id}/02-initial-plan.md
Your coding session operates as a repeatable cycle:
### 1. Generate: Run the agent to produce code for the current PR scope.
### 2. Review: Carefully read the generated code; validate correctness, style,
and merge safety.
### 3. Correct: Fix errors, add missing pieces, or tweak for clarity — either by:
— Making quick manual edits for trivial fixes, or
— Noting recurring or major gaps that merit a prompt update.
### 4. Decide: If manual fixes become frequent or fundamental, update your
prompt artifact to improve future output.
### 5. Stage & Commit: Stage your changes to create a stable baseline before
committing.
### 6. Open PR: Submit pull requests incrementally for peer or lead review,
emphasizing small, safe, and well-justified increments.
### 7. Repeat: Move through each plan segment and pull request until the full
track is complete.
Tips for success:
Trust but verify: Use your human judgment to balance prompt iteration
with tactical manual edits.
Play to your team’s culture: Leverage feature flags and trunk-based
development to safely integrate new code in production.
Keep artifacts up-to-date: Prompt updates are a force multiplier — invest
time refining when it boosts productivity and safety.
Iterate efficiently: Don’t aim for perfect first attempts. Use the “three
reads” mindset you practiced in Planning to guide code review and
prompt tuning.
Communicate: Keep your team looped in by regularly pushing your
prompt and code artifacts, enabling shared ownership and gradual
improvement.
Why detail matters here: Execution may feel “just coding,
” but in practice it’s
where your prompt engineering meets software craftsmanship. You
orchestrate LLM outputs, developer expertise, and continuous feedback —
all while maintaining velocity and quality in complex enterprise systems.
## 8. Measuring Success
Implementing Vibe Engineering is a strategic investment in your team’s
productivity and the long-term quality of your codebase. But any investment
needs to show a return. So, how do we measure the impact of something as
seemingly intangible as “vibe”? We start with what you should already be
tracking: the DORA metrics.
Developed by the DevOps Research and Assessment (DORA) team, these four
key metrics are the gold standard for high-performing technology
organizations. They are:
Deployment Frequency: How often an organization successfully releases
to production.
Lead Time for Changes: The amount of time it takes a commit to get into
production.
Change Failure Rate: The percentage of deployments causing a failure in
production.
Time to Restore Service: How long it takes an organization to recover
from a failure in production.
The question then becomes, does “Vibe Engineering” positively influence
these metrics? We’d expect that a team with a well-engineered vibe would
see a shorter lead time for changes, a lower change failure rate, and a faster
time to restore service.
But how do you really know if this is working to enhance the productivity of
your software development teams?” you might ask, with a skeptical eyebrow
raise. The answer is both simpler and more complex than you’d think: You
ask them.
Before you dismiss this as unscientific, let’s consider the multi-dimensional
nature of developer productivity, as articulated by frameworks like SPACE
(Satisfaction & well-being, Performance, Activity, Communication &
collaboration, and Efficiency & flow). This framework argues that no single
metric can capture productivity; instead, a holistic view encompassing
crucial qualitative data is required.
Engineers, known for their pragmatic and often frank assessments, possess
invaluable insights into the daily realities of software development. They are
the frontline experts experiencing friction points, workflow bottlenecks, and
systemic inefficiencies. Therefore, systematically consulting them is not
merely a formality but a critical strategic imperative. Their candid
perspectives on ‘what works’ and ‘what doesn’t’ within the development
process are the most reliable indicators for structuring business for success.
Building on this understanding, the emerging field of Developer Experience
(DevEx) focuses on systematically identifying and removing the obstacles
that hinder engineering effectiveness. This involves actively listening to
developers to uncover and address issues like tangled dependencies, slow
build times, or ambiguous requirements. By leveraging the direct input of
engineers as critical partners, organizations can unlock profound gains in
innovation, speed, and overall operational excellence.

All of this is not to say that the more granular, practice-specific metrics are
without value. For organizations that may not yet have the maturity to track
DORA metrics or conduct regular qualitative surveys, a “starter kit” of
metrics can be a useful way to begin measuring the impact of Vibe
Engineering.

These metrics, which align with the maturation of AI adoption, can provide
a framework for assessing whether the practice is driving desired
productivity gains and fostering a culture of continuous improvement.
Early Stage (Experimentation & Safety):
Prompt Adoption Rate: Percentage of new tasks initiated using a version-
controlled prompt.
No-Blame Review Sessions: Count of dedicated team review sessions for
AI outputs, focused on prompt improvement rather than individual
blame.
### Mid-Stage (Architecture & Collaboration):
Shared Prompt Contribution Rate: Number of new or updated prompt
artifacts contributed to shared repositories per week/sprint.
Prompt Reusability Index: Frequency with which shared prompts are
reused across different projects or by different team members.
Advanced Stage (Impact & Efficiency):
Iteration Reduction: Average reduction in iterations needed to achieve
desired AI output for a given task type (e.g., planning, code generation).
No-Blame Post-Mortem Frequency: Tracking the occurrence of
blameless post-mortems following AI-assisted failures, indicating a
psychologically safe environment for experimentation.
Prompt-Driven Code Quality: Metrics linking the use of mature prompts
to improved code quality (e.g., fewer bugs in AI-generated sections).
Versioned Prompt Adoption Rate: The percentage of AI-assisted tasks
that utilize version-controlled planning prompts and architectural rules,
reflecting the shift towards prompts as first-class architectural artifacts.
## 9. Advancing Y our Vibe Engineering Practice
This field manual has laid out the foundational principles and a structured
lifecycle for Vibe Engineering, transforming AI-assisted coding from a “vibe”
into a disciplined, scalable practice. You now have a proven recipe for
introducing supervised agentic coding into your enterprise workflows,
grounded in the understanding that lasting advantage comes from
redesigning core processes, not just adding tools.
As you begin or continue to implement Vibe Engineering within your team,
consider these pathways for sustained success and continuous
improvement:
## Start Small, Iterate Often
Begin by applying the Prework, Planning, and Execution phases to a single,
manageable project or a well-defined task. Focus on perfecting the prompt
engineering loop within that narrow scope before expanding. Remember,
the goal is supervised speed, not reckless acceleration.
Prioritize “Prompt as Architecture”
Internalize the concept that your prompts are not disposable hacks, but
version-controlled architectural artifacts. Invest in refining and reusing your
planning prompts and context-setting rules, as these will amplify
institutional memory and decision quality across your team. This is how you
build a reusable, extensible knowledge base.
Foster a Culture of Blameless Experimentation
As a leader, provide the “immunosuppressants” necessary to protect your
teams as they experiment. For technologists, embrace failures as learning
opportunities, refining prompts and processes based on what goes wrong.
This psychological safety is crucial for a generative culture to thrive. It’s okay
to fail fast, as long as you learn faster.
Champion Shared Artifacts
Actively build and contribute to shared prompt repositories and
architectural documentation (like a dedicated .development-context/rules
folder in your projects). This codifies what works and reduces “prompt-
flailing,
” ensuring that lessons learned by one developer benefit the entire
team. Your shared context is your shared superpower.
Measure and Adapt
While the risks of increased Change Failure Rate with unsupervised AI are
real, Vibe Engineering aims to improve lead time without sacrificing
stability. Continuously evaluate your team’s performance, refine your
prompts, and adapt your Vibe Engineering practices based on real-world
outcomes. What gets measured gets improved.
Engage with Y our Peers
This is a rapidly evolving field, and collective intelligence is paramount.
Share your successes, challenges, and modifications with the broader
community. The playbook for effective AI-assisted coding is being written
collaboratively. Your insights can shape the future.
As we collectively move forward, the practical application of the Vibe
Engineering Development Lifecycle to new, complex challenges will be
central to our progress. I’m continuously refining these approaches and
always keen to learn from the experiences and questions of fellow
practitioners and leaders as we navigate these emergent frontiers — feel free
to connect if you’re exploring similar advanced strategies.
To continue the conversation or connect on these topics, you can find me on:
Threads, Bluesky or, LinkedIn.
The future of software development involves deeply integrated AI
collaborators. By treating communication as code and engineering the
“vibe” of your agentic workflows, you’re not just building software; you’re
building a smarter, more efficient way to build software.
Let’s continue to engineer the interface between human ingenuity and AI
capability, together, exploring these and many other emergent frontiers of
AI-assisted engineering.
## 10. Where We Go From Here
This field manual is a starting point, not a final destination. The practices of
AI-assisted engineering are evolving in real-time, and the most valuable
insights come from applying these patterns in the wild and sharing the
results.

## From the Author’s Archives
If you found the thinking here useful, you might also appreciate these past
explorations into the realities of a modern tech career:
Career Advice Nobody Gave Me: Never Ignore a Recruiter — A defense of
the cold-call, and a case for why the recruiters who interrupt your day are
a valuable, misunderstood signal.
Professional Development is a Choice — On the uncomfortable truth that
once you’re a professional, nobody is making you do the homework
anymore — and why that’s both a risk and an opportunity.

## 11. References and Further Reading
Books & Reports
Accelerate: The Science of Lean Software and DevOps by Nicole Forsgren, Jez
Humble, and Gene Kim
The Manager’s Path: A Guide for Tech Leaders Navigating Growth and Change
by Camille Fournier
Turn the Ship Around!: A True Story of Turning Followers into Leaders by L.
David Marquet
The Effective Executive: The Definitive Guide to Getting the Right Things Done
by Peter Drucker
Software Engineering at Google: Lessons Learned from Programming Over
Time by Titus Winters, Tom Manshreck, and Hyrum Wright
Measure What Matters by John Doerr
Chaos Engineering: System Resiliency in Practice by Casey Rosenthal, Nora
Jones
GitClear (2023). Coding on Copilot: 2023 Data Suggests Downward Pressure
on Code Quality.
McKinsey & Company. The state of AI: How organizations are rewiring to
capture value.
McKinsey & Company. Rewired and Running Ahead: Digital and AI leaders
are leaving the rest behind.
METR (2025) Measuring the Impact of Early-2025 AI on Experienced
Open-Source Developer Productivity
Nicole Forsgren, Margaret-Anne Storey, et al. (March 6, 2021) The SPACE
of Developer Productivity: There’s more to it than you think. ACM Queue
Volume 6, Issue 21. https://queue.acm.org/detail.cfm?id=3454124
Blogs, Articles, and Anonymous Forum Chatter
Simon Sharwood. Vibe coding service Replit deleted user’s production
database, faked data, told fibs galore.
https://www.theregister.com/2025/07/21/replit_saastr_vibe_coding_incide
nt/
Cecily Mauran. Google Gemini deletes user’s code: ‘I have failed you
completely and catastrophically’
. https://mashable.com/article/google-
gemini-deletes-users-code
Anonymous users. Forced AI nonsense hysteria happening at your company?
https://www.teamblind.com/post/forced-ai-nonsense-hysteria-
happening-at-your-company-l5amqlml
Gergely Orosz. Cursor makes developers less effective?
https://newsletter.pragmaticengineer.com/p/cursor-makes-developers-
less-effective
Planview. What are DORA Metrics?
https://www.planview.com/resources/articles/what-are-dora-metrics/
Wikipedia editors. Gartner hype cycle.
https://en.wikipedia.org/wiki/Gartner_hype_cycle
Wikipedia editors. npm left-pad incident
https://en.wikipedia.org/wiki/Npm_left-pad_incident
## T ools & Frameworks
Cursor: https://cursor.sh/
Cursor Rules: https://docs.cursor.com/en/context/rules#rules
DORA (DevOps Research and Assessment): https://dora.dev/
DORA Metrics Overview: https://dora.dev/guides/dora-metrics-four-keys/
AI Leadership Software Development Productivity T echnology

### Instructions

missing: provide a concise, human readable description of each PR where you explain what is being done at a
"summary level" listing filenames and model changes is not enough. We must explain to the human reading
this plan what we're trying to do and… 

### Finally

Consider asking for a "summary of test cases" that will allow you to conceptualize the boundaries of what this
PR will be impacting.
- provide a summary of test cases we will introduce or update in this PR. The format should include a test case
name… more

### Create

note that these prompts are written as exemplars and will work, but there are techniques to make these
function even better. I'll be diving into detail on that in a future article, but if you read something like the
chatgpt prompting guide you may… more

