from flask_admin import Admin

from market.index import db, app
from market.models import Category, Product, Tag, User, UserRole
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose, AdminIndexView, Admin
from flask_login import logout_user, current_user
from flask import redirect


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class ProductView(ModelView):  # ctrl+click
    can_view_details = True


class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')


class StatsView(BaseView):
    @expose('/')
    def __index__(self):
        logout_user()
        return self.render('base.html')

    def is_accessible(self):
        return current_user.is_authenticated


admin = Admin(app=app, name='Login', template_mode='bootstrap4',
              index_view=MyAdminIndexView())


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')#chuyển trang

    def is_accessible(self):
        return current_user.is_authenticated  # hiển thị khi đã đăng nhập


admin.add_view(AuthenticatedModelView(Category, db.session, name='Danh mục'))
admin.add_view(AuthenticatedModelView(Product, db.session, name='Sản phẩm'))
admin.add_view(AuthenticatedModelView(Tag, db.session, name='Nhãn'))
admin.add_view(AuthenticatedModelView(User, db.session, name='Người dùng'))
admin.add_view(LogoutView(name='Đăng xuất'))

