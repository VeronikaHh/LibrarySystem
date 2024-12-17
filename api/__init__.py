import importlib
import pkgutil

# Import all submodules at runtime
# This import will be used by alembic to collect all models and build the migrations
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    importlib.import_module(__name__ + "." + module_name)