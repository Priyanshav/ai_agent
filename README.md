# AI Assistant

A small command-line chat assistant built with the OpenAI-compatible chat
completions API. The model is configured through environment variables, and
the assistant can call Python functions registered in `tools.py`.

## What I have learned

### Tool calling

Tool calling lets the model request that the application run a function. The
model does not run Python code itself:

1. The application sends the conversation and the available tool definitions
   to the model.
2. The model either replies normally or returns one or more tool calls, with a
   function name and arguments.
3. The application finds each function in its function map, runs it, and sends
   the result back as a `tool` message. The result includes the matching tool
   call ID.
4. The application asks the model again so it can use the result to answer.

In this project, `TOOLS` describes the functions the model may request, and
`FN_NAME_TO_FN_MAP` connects those names to Python functions. See `tools.py`.

### Parallel tool calling

The model may return several tool calls in a single response. For example, it
could ask for two independent pieces of information at once. The application
can run independent functions concurrently, then send all their results back
to the model.

Receiving multiple tool calls does **not** make their execution parallel by
itself. In this project, the `for tool_call in msg.tool_calls` loop runs each
function one at a time. True parallel execution would require application code
that schedules the calls concurrently. Calls that depend on each other's
results must remain sequential.

### Chained tool calling

Sometimes a tool result leads the model to request another tool. Chained tool
calling means repeating the request → run tool → return result cycle until the
model produces a normal assistant response.

The bounded `for` loop in `ai_assistant.py` implements this cycle: after
sending tool results, it calls the model again; it exits when the response has
no more tool calls or the configured maximum number of rounds is reached. A
chain can therefore require multiple model requests, adding latency.

### Stateless model requests and conversation memory

The chat-completions request does not automatically remember earlier requests.
The application provides context by sending the conversation messages again
with each request.

This project keeps a `messages` list in Python memory. It starts with a system
message, appends each user message, and appends assistant and tool messages as
the conversation continues. Sending that history lets the model respond with
the prior conversation in context.

Because `messages` only lives in the running process, it is lost when the
program exits. Persistent memory would require saving and restoring messages,
for example from a local file or database. The history also grows with every
turn, so keeping it bounded or summarizing older turns can reduce request size
and processing time.

## Project files

- `ai_assistant.py` runs the chat loop, sends requests, and processes tool calls.
- `tools.py` defines available functions, their tool schemas, and the function
  name map.
- `.env` supplies configuration such as `BASE_URL`, `API_KEY`, and `MODEL`.
  Keep credentials private; do not commit real secrets.

## Running

Install the project's Python dependencies, configure the required values in
`.env`, then run:

```powershell
python ai_assistant.py
```

Enter `exit`, `quit`, `bye`, or `goodbye` to end the chat.
