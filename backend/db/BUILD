py_test(
    name = "TestSqlLite",
    srcs = ["TestSqlLite.py"],
    deps = [":SqlLite"],
)

py_library(
    name = "SqlLite",
    srcs = ["SqlLite.py"],
    visibility = ["//backend:__subpackages__"],
    deps = ["//backend/datatype:Log"],
)
