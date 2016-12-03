# -*- coding: utf-8 -*-

from datetime import datetime
import json
from flask import render_template, redirect, flash, \
    url_for, request, current_app, jsonify
from flask_login import login_required, current_user
from . import admin
from ..models import ArticleType, Article, Menu, ArticleTypeSetting
from .forms import SubmitArticlesForm, ManageArticlesForm, DeleteArticleForm, \
    DeleteArticlesForm, AddArticleTypeForm, \
    EditArticleTypeForm, AddArticleTypeNavForm, EditArticleNavTypeForm, SortArticleNavTypeForm, \
    ChangePasswordForm, EditUserInfoForm
from .. import db


@admin.route('/')
@login_required
def manager():
    return redirect(url_for('admin.custom_blog_info'))


@admin.route('/submit-articles', methods=['GET', 'POST'])
@login_required
def submitArticles():
    form = SubmitArticlesForm()

    types = [(t.id, t.name) for t in ArticleType.query.all()]
    form.types.choices = types

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        type_id = form.types.data
        summary = form.summary.data

        articleType = ArticleType.query.get(type_id)

        if articleType:
            article = Article(title=title, content=content, summary=summary,
                              articleType=articleType)
            db.session.add(article)
            db.session.commit()
            flash('发表博文成功！', 'success')
            article_id = Article.query.filter_by(title=title).first().id
            return redirect(url_for('main.articleDetails', id=article_id))
    if form.errors:
        flash('发表博文失败', 'danger')

    return render_template('admin/submit_articles.html', form=form)


@admin.route('/edit-articles/<int:id>', methods=['GET', 'POST'])
@login_required
def editArticles(id):
    article = Article.query.get_or_404(id)
    form = SubmitArticlesForm()

    types = [(t.id, t.name) for t in ArticleType.query.all()]
    form.types.choices = types

    if form.validate_on_submit():
        articleType = ArticleType.query.get_or_404(int(form.types.data))
        article.articleType = articleType

        article.title = form.title.data
        article.content = form.content.data
        article.summary = form.summary.data
        article.update_time = datetime.utcnow()
        db.session.add(article)
        db.session.commit()
        flash('博文更新成功！', 'success')
        return redirect(url_for('main.articleDetails', id=article.id))
    form.title.data = article.title
    form.content.data = article.content
    form.types.data = article.articleType_id
    form.summary.data = article.summary
    return render_template('admin/submit_articles.html', form=form)


@admin.route('/manage-articles', methods=['GET', 'POST'])
@login_required
def manage_articles():
    types_id = request.args.get('types_id', -1, type=int)
    form = ManageArticlesForm(request.form, types=types_id)
    form2 = DeleteArticleForm()  # for delete an article
    from3 = DeleteArticlesForm()  # for delete articles

    types = [(t.id, t.name) for t in ArticleType.query.all()]
    types.append((-1, '全部分类'))
    form.types.choices = types

    pagination_search = 0

    if form.validate_on_submit() or \
            (request.args.get('types_id') is not None):
        if form.validate_on_submit():
            types_id = form.types.data
            page = 1
        else:
            types_id = request.args.get('types_id', type=int)
            form.types.data = types_id
            page = request.args.get('page', 1, type=int)

        result = Article.query.order_by(Article.create_time.desc())
        if types_id != -1:
            articleType = ArticleType.query.get_or_404(types_id)
            result = result.filter_by(articleType=articleType)
        pagination_search = result.paginate(
                page, per_page=current_app.config['ARTICLES_PER_PAGE'], error_out=False)

    if pagination_search != 0:
        pagination = pagination_search
        articles = pagination_search.items
    else:
        page = request.args.get('page', 1, type=int)
        pagination = Article.query.order_by(Article.create_time.desc()).paginate(
                page, per_page=current_app.config['ARTICLES_PER_PAGE'],
                error_out=False)
        articles = pagination.items

    return render_template('admin/manage_articles.html', Article=Article,
                           articles=articles, pagination=pagination,
                           endpoint='admin.manage_articles',
                           form=form, form2=form2, form3=from3,
                           types_id=types_id, page=page)


@admin.route('/manage-articles/delete-article', methods=['GET', 'POST'])
@login_required
def delete_article():
    types_id = request.args.get('types_id', -1, type=int)
    form = DeleteArticleForm()

    if form.validate_on_submit():
        articleId = int(form.articleId.data)
        article = Article.query.get_or_404(articleId)
        count = article.comments.count()
        for comment in article.comments:
            db.session.delete(comment)
        db.session.delete(article)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('删除失败！', 'danger')
        else:
            flash('成功删除博文和%s条评论！' % count, 'success')
    if form.errors:
        flash('删除失败！', 'danger')

    return redirect(url_for('admin.manage_articles', types_id=types_id,
                            page=request.args.get('page', 1, type=int)))


@admin.route('/manage-articles/delete-articles', methods=['GET', 'POST'])
@login_required
def delete_articles():
    types_id = request.args.get('types_id', -1, type=int)
    form = DeleteArticlesForm()

    if form.validate_on_submit():
        articleIds = json.loads(form.articleIds.data)
        count = 0
        for articleId in articleIds:
            article = Article.query.get_or_404(int(articleId))
            db.session.delete(article)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            flash('删除失败！', 'danger')
        else:
            flash('成功删除%s篇博文！' % len(articleIds), 'success')
    if form.errors:
        flash('删除失败！', 'danger')

    return redirect(url_for('admin.manage_articles', types_id=types_id,
                            page=request.args.get('page', 1, type=int)))


@admin.route('/manage-articleTypes', methods=['GET', 'POST'])
@login_required
def manage_articleTypes():
    form = AddArticleTypeForm(menus=-1)
    form2= EditArticleTypeForm()

    menus = Menu.return_menus()
    return_setting_hide = ArticleTypeSetting.return_setting_hide()
    form.menus.choices = menus
    form.setting_hide.choices = return_setting_hide
    form2.menus.choices = menus
    form2.setting_hide.choices = return_setting_hide

    page = request.args.get('page', 1, type=int)

    if form.validate_on_submit():
        name = form.name.data
        articleType = ArticleType.query.filter_by(name=name).first()
        if articleType:
            flash('添加分类失败！该分类名称已经存在。', 'danger')
        else:
            introduction = form.introduction.data
            setting_hide = form.setting_hide.data
            menu = Menu.query.get(form.menus.data)
            if not menu:
               menu = None
            articleType = ArticleType(name=name, introduction=introduction, menu=menu,
                                      setting=ArticleTypeSetting(name=name))
            if setting_hide == 1:
                articleType.setting.hide = True
            if setting_hide == 2:
                articleType.setting.hide = False
            # Note: to check whether introduction or menu is existing or not,
            # just use if `articleType.introduction` or `if articleType.menu`.
            db.session.add(articleType)
            db.session.commit()
            flash('添加分类成功！', 'success')
        return redirect(url_for('.manage_articleTypes'))
    if form.errors:
        flash('添加分类失败！请查看填写有无错误。', 'danger')
        return redirect(url_for('.manage_articleTypes'))

    pagination = ArticleType.query.order_by(ArticleType.id.desc()).paginate(
        page, per_page=current_app.config['COMMENTS_PER_PAGE'],
        error_out=False)
    articleTypes = pagination.items
    return render_template('admin/manage_articleTypes.html', articleTypes=articleTypes,
                           pagination=pagination, endpoint='.manage_articleTypes',
                           form=form, form2=form2, page=page)


@admin.route('/manage-articletypes/edit-articleType', methods=['POST'])
def edit_articleType():
    form2= EditArticleTypeForm()

    menus = Menu.return_menus()
    setting_hide = ArticleTypeSetting.return_setting_hide()
    form2.menus.choices = menus
    form2.setting_hide.choices = setting_hide

    page = request.args.get('page', 1, type=int)

    if form2.validate_on_submit():
        name = form2.name.data
        articleType_id = int(form2.articleType_id.data)
        articleType = ArticleType.query.get_or_404(articleType_id)
        setting_hide = form2.setting_hide.data

        if articleType.is_protected:
            if form2.name.data != articleType.name or \
                            form2.introduction.data != articleType.introduction:
                flash('您只能修改系统默认分类的属性和所属导航！', 'danger')
            else:
                menu = Menu.query.get(form2.menus.data)
                if not menu:
                    menu = None
                articleType.menu = menu
                if setting_hide == 1:
                    articleType.setting.hide = True
                if setting_hide == 2:
                    articleType.setting.hide = False
                db.session.add(articleType)
                db.session.commit()
                flash('修改系统默认分类成功！', 'success')
        elif ArticleType.query.filter_by(name=form2.name.data).first() \
            and ArticleType.query.filter_by(name=form2.name.data).first().id != articleType_id:
                flash('修改分类失败！该分类名称已经存在。', 'danger')
        else:
            introduction = form2.introduction.data
            menu = Menu.query.get(form2.menus.data)
            if not menu:
               menu = None
            articleType = ArticleType.query.get_or_404(articleType_id)
            articleType.name = name
            articleType.introduction = introduction
            articleType.menu = menu
            if not articleType.setting:
                articleType.setting = ArticleTypeSetting(name=articleType.name)
            if setting_hide == 1:
                    articleType.setting.hide = True
            if setting_hide == 2:
                articleType.setting.hide = False

            db.session.add(articleType)
            db.session.commit()
            flash('修改分类成功！', 'success')
        return redirect(url_for('.manage_articleTypes', page=page))
    if form2.errors:
        flash('修改分类失败！请查看填写有无错误。', 'danger')
        return redirect(url_for('.manage_articleTypes', page=page))


@admin.route('/manage-articleTypes/delete-articleType/<int:id>')
@login_required
def delete_articleType(id):
    page = request.args.get('page', 1, type=int)

    articleType = ArticleType.query.get_or_404(id)
    if articleType.is_protected:
        flash('警告：您没有删除系统默认分类的权限！', 'danger')
        return redirect(url_for('admin.manage_articleTypes', page=page))
    count = 0
    systemType = ArticleTypeSetting.query.filter_by(protected=True).first().types.first()
    articleTypeSetting = ArticleTypeSetting.query.get(articleType.setting_id)
    for article in articleType.articles.all():
        count += 1
        article.articleType_id = systemType.id
        db.session.add(article)
        db.session.commit()
    if articleTypeSetting:
        db.session.delete(articleTypeSetting)
    db.session.delete(articleType)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        flash('删除分类失败！', 'danger')
    else:
        flash('删除分类成功！同时将原来该分类的%s篇博文添加到<未分类>。' % count, 'success')
    return redirect(url_for('admin.manage_articleTypes', page=page))


@admin.route('/manage-articleTypes/get-articleType-info/<int:id>')
@login_required
def get_articleType_info(id):
    if request.is_xhr:
        articletype = ArticleType.query.get_or_404(id)
        if articletype.is_hide:
            setting_hide = 1
        else:
            setting_hide = 2
        return jsonify({
            'name': articletype.name,
            'setting_hide': setting_hide,
            'introduction': articletype.introduction,
            'menu': articletype.menu_id or -1
        })


@admin.route('/manage-articleTypes/nav', methods=['GET', 'POST'])
@login_required
def manage_articleTypes_nav():
    form = AddArticleTypeNavForm()
    form2 = EditArticleNavTypeForm()
    form3 = SortArticleNavTypeForm()

    page = request.args.get('page', 1, type=int)
    if form.validate_on_submit():
        name = form.name.data
        menu = Menu.query.filter_by(name=name).first()
        if menu:
            page = page
            flash('添加导航失败！该导航名称已经存在。', 'danger')
        else:
            menu_count = Menu.query.count()
            menu = Menu(name=name, order=menu_count+1)
            db.session.add(menu)
            db.session.commit()
            page = -1
            flash('添加导航成功！', 'success')
        return redirect(url_for('admin.manage_articleTypes_nav', page=page))
    if page == -1:
        page = (Menu.query.count() - 1) // \
               current_app.config['COMMENTS_PER_PAGE'] + 1
    pagination = Menu.query.order_by(Menu.order.asc()).paginate(
            page, per_page=current_app.config['COMMENTS_PER_PAGE'],
            error_out=False)
    menus = pagination.items
    return render_template('admin/manage_articleTypes_nav.html', menus=menus,
                           pagination=pagination, endpoint='.manage_articleTypes_nav',
                           page=page, form=form, form2=form2, form3=form3)


@admin.route('/manage-articleTypes/nav/edit-nav', methods=['GET', 'POST'])
@login_required
def edit_nav():
    form2 = EditArticleNavTypeForm()

    page = request.args.get('page', 1, type=int)

    if form2.validate_on_submit():
        name = form2.name.data
        nav_id = int(form2.nav_id.data)
        if Menu.query.filter_by(name=name).first() \
            and Menu.query.filter_by(name=name).first().id != nav_id:
                flash('修改导航失败！该导航名称已经存在。', 'danger')
        else:
            nav = Menu.query.get_or_404(nav_id)
            nav.name = name
            db.session.add(nav)
            db.session.commit()
            flash('修改导航成功！', 'success')
        return redirect(url_for('admin.manage_articleTypes_nav', page=page))
    if form2.errors:
        flash('修改导航失败！请查看填写有无错误。', 'danger')
        return redirect(url_for('admin.manage_articleTypes_nav', page=page))


@admin.route('/manage-articleTypes/nav/delete-nav/<int:id>')
@login_required
def delete_nav(id):
    page = request.args.get('page', 1, type=int)

    nav = Menu.query.get_or_404(id)
    count = 0
    for articleType in nav.types.all():
        count += 1
        articleType.menu = None
        db.session.add(articleType)
    nav.sort_delete()
    db.session.delete(nav)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        flash('删除导航失败！', 'danger')
    else:
        flash('删除导航成功！同时将原来该导航的%s种分类的导航设置为无。' % count, 'success')
    return redirect(url_for('admin.manage_articleTypes_nav', page=page))


@admin.route('/manage-articleTypes/nav/sort-up/<int:id>')
@login_required
def nav_sort_up(id):
    page = request.args.get('page', 1, type=int)

    menu = Menu.query.get_or_404(id)
    pre_menu = Menu.query.filter_by(order=menu.order-1).first()
    if pre_menu:
        (menu.order, pre_menu.order) = (pre_menu.order, menu.order)
        db.session.add(menu)
        db.session.add(pre_menu)
        db.session.commit()
        flash('成功将该导航升序！', 'success')
    else:
        flash('该导航已经位于最前面！', 'danger')
    return redirect(url_for('admin.manage_articleTypes_nav', page=page))


@admin.route('/manage-articleTypes/nav/sort-down/<int:id>')
@login_required
def nav_sort_down(id):
    page = request.args.get('page', 1, type=int)

    menu = Menu.query.get_or_404(id)
    latter_menu = Menu.query.filter_by(order=menu.order+1).first()
    if latter_menu:
        (latter_menu.order, menu.order) = (menu.order, latter_menu.order)
        db.session.add(menu)
        db.session.add(latter_menu)
        db.session.commit()
        flash('成功将该导航降序！', 'success')
    else:
        flash('该导航已经位于最后面！', 'danger')
    return redirect(url_for('admin.manage_articleTypes_nav', page=page))


@admin.route('/manage-articleTypes/get-articleTypeNav-info/<int:id>')
@login_required
def get_articleTypeNav_info(id):
    if request.is_xhr:
        menu = Menu.query.get_or_404(id)
        return jsonify({
            'name': menu.name,
            'nav_id': menu.id,
        })


@admin.route('/account/')
@login_required
def account():
    form = ChangePasswordForm()
    form2 = EditUserInfoForm()

    return render_template('admin/admin_account.html',
                           form=form, form2=form2)


@admin.route('/account/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('修改密码成功！', 'success')
            return redirect(url_for('admin.account'))
        else:
            flash('修改密码失败！密码不正确！', 'danger')
            return redirect(url_for('admin.account'))


@admin.route('/account/edit-user-info', methods=['GET', 'POST'])
@login_required
def edit_user_info():
    form2 = EditUserInfoForm()

    if form2.validate_on_submit():
        if current_user.verify_password(form2.password.data):
            current_user.username = form2.username.data
            current_user.email = form2.email.data
            db.session.add(current_user)
            db.session.commit()
            flash('修改用户信息成功！', 'success')
            return redirect(url_for('admin.account'))
        else:
            flash('修改用户信息失败！密码不正确！', 'danger')
            return redirect(url_for('admin.account'))
