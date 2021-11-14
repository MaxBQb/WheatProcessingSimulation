import inject

import view.base
import view.workers
import view.utils
from config import make_config, Config
from database import Database
import model
from database_observer import DatabaseObserver
from mappers import table_to_model


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
    view.utils.init_theme()
    view.workers.WorkersView().run()


def configure(binder: inject.Binder):
    # Couple of components
    # Handled at runtime
    binder.bind(Config, make_config("config.yaml"))


inject.configure(configure)

if __name__ == '__main__':
    main()
