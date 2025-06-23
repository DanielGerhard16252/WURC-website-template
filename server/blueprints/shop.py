from flask import Blueprint, render_template, flash, redirect, url_for
from db_schema import Admin, ShopItem, db
from flask_login import login_required, current_user
from server.forms.shop_forms import ShopItemForm

shop_bp = Blueprint('shop', __name__, template_folder='templates/shop')

@shop_bp.route('/')
def shop():
    items = ShopItem.query.order_by(ShopItem.name.asc()).all()
    return render_template('shop/shop.html', items=items)  # , items=items

@shop_bp.route('/<int:item_id>')
def shop_item(item_id):
    item = ShopItem.query.get_or_404(item_id)
    return render_template('shop/shop_item.html', item=item)

@shop_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_shop_item():
    """
    GET: Displays the form to create a new shop item.
    POST: Handles the creation of a new shop item.
    """
    if not current_user.is_authenticated:
        flash("You do not have permission to create shop items.", "danger")
        return redirect(url_for('shop.shop'))

    form = ShopItemForm()

    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        price = form.price.data

        new_item = ShopItem(name=name, description=description, price=price, creator_id=current_user.id)
        db.session.add(new_item)
        db.session.commit()

        flash("Shop item created successfully!", "success")
        return redirect(url_for('shop.shop'))

    return render_template("shop/create_shop_item.html", form=form)

@shop_bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_shop_item(item_id):
    """
    GET: Displays the form to edit an existing shop item.
    POST: Handles the update of an existing shop item.
    """
    item = ShopItem.query.get_or_404(item_id)

    form = ShopItemForm(obj=item)

    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.price = form.price.data
        db.session.commit()

        flash("Shop item updated successfully!", "success")
        return redirect(url_for('shop.shop'))

    return render_template("shop/edit_shop_item.html", form=form, item=item)

@shop_bp.route('/delete/<int:item_id>')
@login_required
def delete_shop_item(item_id):
    """
    GET: Deletes a shop item. (yes I know I should use DELETE but this is simpler for now)
    """
    item = ShopItem.query.get_or_404(item_id)

    db.session.delete(item)
    db.session.commit()

    flash("Shop item deleted successfully!", "success")
    return redirect(url_for('shop.shop'))

