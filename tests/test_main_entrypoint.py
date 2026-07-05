import importlib


def test_main_module_can_be_imported():
    module = importlib.import_module("main")
    assert hasattr(module, "main")
