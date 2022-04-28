from flask import render_template,url_for,flash, redirect,request,Blueprint
from flask_login import current_user,login_required
from equipmentsupply import db
from equipmentsupply.models import EquipmentPost
from equipmentsupply.equipment_posts.forms import EquipmentPostForm

equipment_posts = Blueprint('equipment_posts',__name__)

@equipment_posts.route('/create',methods=['GET','POST'])
@login_required
def create_post():
    form = EquipmentPostForm()

    if form.validate_on_submit():

        equipment_post = EquipmentPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id
                             )
        db.session.add(equipment_post)
        db.session.commit()
        flash("Equipment Post Created")
        return redirect(url_for('core.index'))

    return render_template('create_post.html',form=form)


# int: makes sure that the equipment_post_id gets passed as in integer
# instead of a string so we can look it up later.
@equipment_posts.route('/<int:equipment_post_id>')
def equipment_post(equipment_post_id):
    # grab the requested equipment post by id number or return 404
    equipment_post = EquipmentPost.query.get_or_404(equipment_post_id)
    return render_template('equipment_post.html',title=equipment_post.title,
                            date=equipment_post.date,post=equipment_post
    )

@equipment_posts.route("/<int:equipment_post_id>/update", methods=['GET', 'POST'])
@login_required
def update(equipment_post_id):
    equipment_post = EquipmentPost.query.get_or_404(equipment_post_id)
    if equipment_post.author != current_user:
        # Forbidden, No Access
        abort(403)

    form = EquipmentPostForm()
    if form.validate_on_submit():
        equipment_post.title = form.title.data
        equipment_post.text = form.text.data
        db.session.commit()
        flash('Post Updated')
        return redirect(url_for('equipment_posts.equipment_post', equipment_post_id=equipment_post.id))
    # Pass back the old equipment post information so they can start again with
    # the old text and title.
    elif request.method == 'GET':
        form.title.data = equipment_post.title
        form.text.data = equipment_post.text
    return render_template('create_post.html', title='Update',
                           form=form)


@equipment_posts.route("/<int:equipment_post_id>/delete", methods=['POST'])
@login_required
def delete_post(equipment_post_id):
    equipment_post = EquipmentPost.query.get_or_404(equipment_post_id)
    if equipment_post.author != current_user:
        abort(403)
    db.session.delete(equipment_post)
    db.session.commit()
    flash('Post has been deleted')
    return redirect(url_for('core.index'))
