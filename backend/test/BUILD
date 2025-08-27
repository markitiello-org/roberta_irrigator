py_binary(
    name = "test_rpc_client",
    srcs = ["test_rpc_client.py"],
    deps = ["@pip//rpyc"],
)

py_binary(
    name = "interactive_rpc_client",
    srcs = ["interactive_rpc_client.py"],
    deps = ["@pip//rpyc"],
)

sh_binary(
    name = "test_server_and_client",
    srcs = ["test_server_and_client.sh"],
    data = [
        ":test_rpc_client",
        "//backend:start",
    ],
)
