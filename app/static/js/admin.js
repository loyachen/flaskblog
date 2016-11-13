//JS For manage-articles when select articles or select comments
$(document).ready(function () {
    $('#select-all').click(function () {
        if ($(this).prop('checked')) {
            $('.op_check').prop('checked', true);
        } else {
            $('.op_check').prop('checked', false);
        }
    });
});

//JS For submit article id to delete article
function delCfm(articleId) {
    $('#cfmClick').click(function () {
        formSubmit(articleId);
    });
    $('#delCfmModel').modal();
}
function formSubmit(articleId) {
    $('#delForm' + articleId).submit();
}

//JS For select articles to delete
$(document).ready(function () {
    $('#delArtsCfm').click(function(){
        $('#delArticlesForm').submit();
    });

    $('#delArticles').click(function () {
        if ($('.op_check').filter(':checked').size() > 0) {
            var articleIds = [];
            $('.op_check:checked').each(function(){
                articleIds.push($(this).val());
            });
            var articleIdsJson = JSON.stringify(articleIds);
            $('#articleIds').val(articleIdsJson);
            $('#delArtsCfmModel').modal();
        } else {
            $('#selArtsCfmModel').modal();
        }
    });
});




//JS For add articleType
$(document).ready(function() {
    $('.add-articleType-btn').click(function() {
        $('#addArticleTypeFormModel').modal();
    });
});

//JS For confirm to delete an articleType
function delArticleTypeCfm(url) {
    $('#delArticleTypeCfmClick').click(function(){
        window.location.href = url;
    });
    $('#delArticleTypeCfmModel').modal();
}

//JS For edit articleType to get its info
function get_articleType_info(url, id) {
    $.getJSON(url, function(data) {
        $('#editName').val(data.name);
        $('#editSetting_hide').val(data.setting_hide);
        $('#editIntroduction').val(data.introduction);
        $('#editMenus').val(data.menu);
        $('#articleType_id').val(id);
        $('#ModalTitle').text('修改博文分类：' + data.name);
        if (data.name == '未分类') {
            $('#editName').prop('readonly', true);
            $('#editIntroduction').prop('readonly', true);
        } else {
            $('#editName').prop('readonly', false);
            $('#editIntroduction').prop('readonly', false);
        }
        $('#editArticleTypeFormModel').modal();
    });
}

//JS For add articleType
$(document).ready(function() {
    $('.add-articleType-nav-btn').click(function() {
        $('#addArticleTypeNavFormModel').modal();
    });
});

//JS For edit articleTypeNav to get its info
function get_articleTypeNav_info(url) {
    $.getJSON(url, function(data) {
        $('#editNavName').val(data.name);
        $('#nav_id').val(data.nav_id);
        $('#NavModalTitle').text('修改分类导航：' + data.name);
        $('#editArticleTypeNavFormModel').modal();
    });
}

//JS For confirm to delete an articleType nav
function delArticleTypeNavCfm(url) {
    $('#delArticleTypeNavCfmClick').click(function(){
        window.location.href = url;
    });
    $('#delArticleTypeNavCfmModel').modal();
}


//JS For change password
function changePassword() {
    $('#changePasswordFormModal').modal();
}

//JS For edit user info
function EditUserInfo() {
    $('#editUserInfoFormModal').modal();
}
