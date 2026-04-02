## Analysis

The agent had four types of memory throughout the conversation:

- Factual Memory: This is the type of memories the model deems as factual, for example, when the user introduces themselves as Alice, the agent saves this as a fact. The same as when she says she's a software engineer.

- Preference Memory: This type of memory is triggered when the user explains something they like/prefer. For example, Alice stated that she prefers Python. Which when the model was asked about it again, it got correct. 
- Episodic Memory: Episodic Memory is when the agent saves events, for example, the user mentioned working on a ML project, which triggers this type of memory. 
- Semantic Memory: Semantic memory is teh Agent's trained memory that is not constricted by the session, it is more of "general knowledge".

It was noticable to see which parts of the conversation triggered the insert_memory. As it was not triggered for every part of the conversation, rather when the query contained user-specific information.

What i found interesting is that each user has their unique memory session, meaning different users can not tap into private conversationsor memories with the Agent.
