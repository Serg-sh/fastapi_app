from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()


class Country(Base):
    __tablename__ = 'country'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    code = Column(String)
    code2 = Column(String)
    code3 = Column(String)
    full_name = Column(String)

    addresses = relationship("Address", back_populates="country")


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    address_line = Column(String)
    address_line1 = Column(String)
    full_address = Column(String)
    postal_code = Column(String)
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
    comment = Column(String)

    country = relationship("Country", back_populates="addresses")
    companies = relationship("Company", back_populates="address")


class Contact(Base):
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    fio = Column(String)
    phone = Column(String)
    email = Column(String)
    comment = Column(String)

    user = relationship("User", back_populates="contact")
    companies = relationship("CompanyContactAssociation", back_populates="contact")


class Company(Base):
    __tablename__ = 'company'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)
    email = Column(String)
    address_id = Column(Integer, ForeignKey('address.id'))
    comment = Column(String)

    address = relationship("Address", back_populates="companies")
    contacts = relationship("CompanyContactAssociation", back_populates="company")
    client_orders = relationship("Order", foreign_keys="Order.client_id", back_populates="client")
    buyer_orders = relationship("Order", foreign_keys="Order.buyer_id", back_populates="buyer")
    proposals = relationship("Proposal", back_populates="client_company")
    files = relationship("FileManager", secondary="company_docs_association", back_populates="companies")


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    type = Column(String)

    file_managers = relationship("FileManager", back_populates="file")


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    number = Column(String, unique=True)
    state = Column(Integer, ForeignKey('orders_states.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    client_id = Column(Integer, ForeignKey('company.id'))
    buyer_id = Column(Integer, ForeignKey('company.id'))
    priority = Column(Integer, ForeignKey('simple_data.id'))
    quantity = Column(Float)
    date_created = Column(DateTime)
    date_start = Column(DateTime)
    date_finish = Column(DateTime)
    date_plan_shipping = Column(DateTime)
    date_shipping = Column(DateTime)
    is_complete = Column(Boolean)
    comment = Column(String)

    state_rel = relationship("OrderState")
    product = relationship("Product")
    client = relationship("Company", foreign_keys=[client_id], back_populates="client_orders")
    buyer = relationship("Company", foreign_keys=[buyer_id], back_populates="buyer_orders")
    priority_rel = relationship("SimpleData")
    proposals = relationship("Proposal", back_populates="order")
    users = relationship("User", secondary="orders_users_association", back_populates="orders")
    files = relationship("FileManager", secondary="orders_docs_association", back_populates="orders")


class OrderState(Base):
    __tablename__ = 'orders_states'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    machine_name = Column(String)


class FileManager(Base):
    __tablename__ = 'file_manager'

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey('files.id'))
    name = Column(String)
    comment = Column(String)

    file = relationship("File", back_populates="file_managers")
    orders = relationship("Order", secondary="orders_docs_association", back_populates="files")
    proposals = relationship("Proposal", secondary="proposal_docs_association", back_populates="files")
    companies = relationship("Company", secondary="company_docs_association", back_populates="files")
    expertises = relationship("Expertise", secondary="expertise_docs_association", back_populates="files")


class Proposal(Base):
    __tablename__ = 'proposal'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    name = Column(String)
    date_created = Column(DateTime)
    quantity = Column(Float)
    client_company_id = Column(Integer, ForeignKey('company.id'))
    product_id = Column(Integer, ForeignKey('product.id'))
    status = Column(Integer, ForeignKey('simple_data.id'))
    comment = Column(String)

    order = relationship("Order", back_populates="proposals")
    client_company = relationship("Company", back_populates="proposals")
    product = relationship("Product")
    status_rel = relationship("SimpleData")
    expertises = relationship("Expertise", back_populates="proposal")
    files = relationship("FileManager", secondary="proposal_docs_association", back_populates="proposals")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String)
    password = Column(String)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    status = Column(Boolean)

    contact = relationship("Contact", back_populates="user")
    roles = relationship("Role", secondary="user_roles_association", back_populates="users")
    departments = relationship("Department", secondary="user_departments_association", back_populates="users")
    roles_groups = relationship("RolesGroup", secondary="users_roles_group_association", back_populates="users")
    orders = relationship("Order", secondary="orders_users_association", back_populates="users")
    expertises = relationship("Expertise", back_populates="user")


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    users = relationship("User", secondary="user_roles_association", back_populates="roles")
    roles_groups = relationship("RolesGroup", back_populates="roles")


class RolesGroup(Base):
    __tablename__ = 'roles_group'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    roles_id = Column(Integer, ForeignKey('roles.id'))

    roles = relationship("Role", back_populates="roles_groups")
    users = relationship("User", secondary="users_roles_group_association", back_populates="roles_groups")


class SimpleList(Base):
    __tablename__ = 'simple_list'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    items = relationship("SimpleData", back_populates="list")


class SimpleData(Base):
    __tablename__ = 'simple_data'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    short = Column(String)
    list_id = Column(Integer, ForeignKey('simple_list.id'))

    list = relationship("SimpleList", back_populates="items")


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    drawing_id = Column(Integer, ForeignKey('drawing.id'))
    workpiec_id = Column(Integer, ForeignKey('workpieces.id'))
    comment = Column(String)

    drawing = relationship("Drawing")
    workpiece = relationship("Workpiece", foreign_keys=[workpiec_id])
    orders = relationship("Order", back_populates="product")
    proposals = relationship("Proposal", back_populates="product")


class Drawing(Base):
    __tablename__ = 'drawing'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    workpiecs_id = Column(Integer, ForeignKey('workpieces.id'))
    appointments_id = Column(Integer, ForeignKey('appointments.id'))
    comment = Column(String)

    workpieces = relationship("Workpiece", foreign_keys=[workpiecs_id])
    appointments = relationship("Appointment")
    products = relationship("Product", back_populates="drawing")


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    drawings = relationship("Drawing", back_populates="appointments")


class Workpiece(Base):
    __tablename__ = 'workpieces'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    comment = Column(String)

    drawings = relationship("Drawing", foreign_keys="Drawing.workpiecs_id", back_populates="workpieces")
    products = relationship("Product", foreign_keys="Product.workpiec_id", back_populates="workpiece")


class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    comment = Column(String)

    users = relationship("User", secondary="user_departments_association", back_populates="departments")
    expertises = relationship("Expertise", back_populates="department")


class Expertise(Base):
    __tablename__ = 'expertise'

    id = Column(Integer, primary_key=True)
    department_id = Column(Integer, ForeignKey('department.id'))
    proposal_id = Column(Integer, ForeignKey('proposal.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    date_created = Column(DateTime)
    date_finish = Column(DateTime)
    status = Column(Integer, ForeignKey('simple_data.id'))
    source = Column(String)
    comment = Column(String)

    department = relationship("Department", back_populates="expertises")
    proposal = relationship("Proposal", back_populates="expertises")
    user = relationship("User", back_populates="expertises")
    status_rel = relationship("SimpleData")
    files = relationship("FileManager", secondary="expertise_docs_association", back_populates="expertises")


# Association tables for many-to-many relationships
class CompanyContactAssociation(Base):
    __tablename__ = 'field_company_contacts'

    company_id = Column(Integer, ForeignKey('company.id'), primary_key=True)
    contact_id = Column(Integer, ForeignKey('contact.id'), primary_key=True)

    company = relationship("Company", back_populates="contacts")
    contact = relationship("Contact", back_populates="companies")


class UserRolesAssociation(Base):
    __tablename__ = 'field_user_roles'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)


class UserDepartmentsAssociation(Base):
    __tablename__ = 'field_user_departments'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    department_id = Column(Integer, ForeignKey('department.id'), primary_key=True)


class OrdersUsersAssociation(Base):
    __tablename__ = 'field_orders_users'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)


class OrdersDocsAssociation(Base):
    __tablename__ = 'field_orders_docs'

    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    file_manager_id = Column(Integer, ForeignKey('file_manager.id'), primary_key=True)


class ProposalDocsAssociation(Base):
    __tablename__ = 'field_proposal_docs'

    proposal_id = Column(Integer, ForeignKey('proposal.id'), primary_key=True)
    file_manager_id = Column(Integer, ForeignKey('file_manager.id'), primary_key=True)


class CompanyDocsAssociation(Base):
    __tablename__ = 'field_company_docs'

    company_id = Column(Integer, ForeignKey('company.id'), primary_key=True)
    file_manager_id = Column(Integer, ForeignKey('file_manager.id'), primary_key=True)


class ExpertiseDocsAssociation(Base):
    __tablename__ = 'field_expertise_docs'

    expertise_id = Column(Integer, ForeignKey('expertise.id'), primary_key=True)
    file_manager_id = Column(Integer, ForeignKey('file_manager.id'), primary_key=True)


class UsersRolesGroupAssociation(Base):
    __tablename__ = 'field_users_roles_group'

    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    roles_group_id = Column(Integer, ForeignKey('roles_group.id'), primary_key=True)