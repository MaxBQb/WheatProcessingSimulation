import inject

import model
from config import make_config, Config
from database import Database
from database_observer import DatabaseObserver
from mappers import table_to_model
from view.base import WindowManager
from view.main_menu import MainMenuView
from view.utils import init_theme


def main():
    db = inject.instance(Database)
    db_observer = inject.instance(DatabaseObserver)
    tables = {
        "contract": model.Contract,
        "legal_entity": model.LegalEntity,
        "machine": model.Machine,
        "production_line": model.ProductionLine,
        "resource": model.Resource,
        "standard": model.Standard,
        "worker": model.Worker,
    }
    query = "SELECT * FROM "
    for table, clazz in tables.items():
        print(table)
        with db.execute(query+table) as cursor:
            for data in cursor:
                a = table_to_model(cursor.column_names, data, clazz)
                print(a)
    db_observer.run()
    init_theme()
    MainMenuView().run()
    inject.instance(WindowManager).run()


def configure(binder: inject.Binder):
    # Couple of components
    # Handled at runtime
    binder.bind(Config, make_config("config.yaml"))


inject.configure(configure)

if __name__ == '__main__':
    main()
