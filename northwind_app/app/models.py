from app import db

class Customer(db.Model):
    __tablename__ = 'Customers'
    CustomerID = db.Column(db.String(5), primary_key=True)
    CompanyName = db.Column(db.String, nullable=False)
    ContactName = db.Column(db.String, nullable=True)
    ContactTitle = db.Column(db.String, nullable=True)
    Address = db.Column(db.String, nullable=True)
    City = db.Column(db.String, nullable=True)
    Region = db.Column(db.String, nullable=True)
    PostalCode = db.Column(db.String, nullable=True)
    Country = db.Column(db.String, nullable=True)
    Phone = db.Column(db.String, nullable=True)
    Fax = db.Column(db.String, nullable=True)

class Category(db.Model):
    __tablename__ = 'Categories'

    CategoryID = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.String(255))
    Picture = db.Column(db.LargeBinary)

    def __repr__(self):
        return f"<Category(CategoryID='{self.CategoryID}', CategoryName='{self.CategoryName}', Description='{self.Description}')>"

class Product(db.Model):
    __tablename__ = 'Products'

    ProductID = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    SupplierID = db.Column(db.Integer)
    CategoryID = db.Column(db.Integer, db.ForeignKey('Categories.CategoryID'))
    UnitPrice = db.Column(db.Float)

    category = db.relationship('Category', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f"<Product(ProductID='{self.ProductID}', ProductName='{self.ProductName}', SupplierID='{self.SupplierID}', CategoryID='{self.CategoryID}', UnitPrice='{self.UnitPrice}')>"

    def serialize(self):
        return {
            'id': self.ProductID,
            'name': self.ProductName,
            'price': self.UnitPrice,
        }
