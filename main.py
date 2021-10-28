import inject
from config import make_config, Config
from database import Database
import model
from mappers import table_to_model


def main():
    db = inject.instance(Database)
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


def configure(binder: inject.Binder):
    # Couple of components
    # Handled at runtime
    binder.bind(Config, make_config("config.yaml"))


inject.configure(configure)

if __name__ == '__main__':
    main()
