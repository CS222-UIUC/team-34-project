from app import db, create_app
from app.models import Category


def init_categories():
    app = create_app()
    with app.app_context():
        # Create default categories
        categories = [
            "Football",
            "Basketball",
            "Baseball",
            "Soccer",
            "Tennis",
            "Golf",
            "Hockey",
            "Rugby",
            "Cricket",
            "Swimming",
        ]

        for category_name in categories:
            category = Category.query.filter_by(name=category_name).first()
            if not category:
                category = Category(name=category_name)
                db.session.add(category)

        db.session.commit()
        print("Categories initialized successfully!")


if __name__ == "__main__":
    init_categories()
