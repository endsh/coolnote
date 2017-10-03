/*
 * web - v1.0.0 - 2017-10-03
 * home: http://www.haoku.net/
 * Copyright (c) 2017 XiaoKu Inc. All Rights Reserved.
 */
+ function ($) {
    "use strict";

    $(function () {
        window.searchAjax = null;
        window.searchTimeout = null;
        function updateTagPanelLeft() {
            $('.tags-panel, .tags-search-panel').css('left', $('.select2-search.select2-search--inline').position().left + 'px');
        }

        var $tags = $('.editor-tags');
        $tags.select2({
            language: 'zh-CN',
            minimumInputLength: 100,
            maximumInputLength: 100,
            tags: true,
            tokenSeparators: [',', ';'],
            placeholder: "标签，如：php 可使用逗号,分号;分隔",
            maximumSelectionLength: 5,
            selectOnClose: false,
            createTag: function () {
                var word = $('.select2-search__field').val();
                if (!!word) {
                    var c = word.charAt(word.length - 1);
                    if (c == ',' || c == ';') {
                        word = word.substring(0, word.length - 1);
                    }
                }
                var tag = $('.tags-search-panel > li > a');
                $('.tags-search-panel').hide();
                if (tag.length > 0 && tag.data('name') === word && !!tag.data('id')) {
                    return { id: tag.data('id'), text: tag.data('name') };
                } else {
                    clearSearchAjax();
                    $.ajax({
                        url: "/tags/search",  
                        data: {
                            word: word
                        },
                        type: 'post',  
                        dataType: 'json',  
                        success: function (data) {
                            if (!data.tags[0].id) {
                                showCreateTagModal(word);
                            } else {
                                insertTag(data.tags[0].id, data.tags[0].name);
                            }
                        }
                    })
                }
            }
        })
        $.each($('.editor-tags option'), function (i, option) {
            insertTag($(option).val(), $(option).text())
        });
        $('.select2-search.select2-search--inline').on('click', function () {
            $('.select2-search__field').val('');
            $('.select2-search__field').focus();
            updateTagPanelLeft();
        });
        $tags.on("select2:opening", function () {
            if (!$('.select2-search__field').val()) {
                updateTagPanelLeft()
                $('.tags-search-panel').hide();
                $('.tags-panel').show();
            }
            return false;
        });
        $tags.on("select2:unselect", function () {
            var val = $tags.val();
            $.each($('.editor-tags option'), function (i, option) {
                if (val === null || val.indexOf($(option).val()) === -1) {
                    $(option).remove()
                } 
            })
        });
        window.chinese = false;
        $(document).on('compositionstart', '.select2-search__field', function () {
            window.chinese = true;
        });
        $(document).on('compositionend', '.select2-search__field', function () {
            window.chinese = false;
        });
        $(document).on('input propertychange', '.select2-search__field', function () {
            if (window.chinese === false) {
                clearSearchAjax();
                clearSearchTimeout();
                var word = $(this).val();
                if (!!word) {
                    var c = word.charAt(word.length - 1);
                    if (c == ',' || c == ';') {
                        word = word.substring(0, word.length - 1);
                    }
                }
                if (!!word) {
                    window.searchTimeout = setTimeout(function () {
                        window.searchAjax = $.ajax({
                            url: "/tags/search",  
                            data: {
                                word: word
                            },
                            type: 'post',  
                            dataType: 'json',  
                            success: function (data) {
                                updateTagPanelLeft();
                                $('.tags-panel').hide();
                                $('.tags-search-panel').html('');
                                $('#tags-search-tmpl').tmpl(data).appendTo('.tags-search-panel');
                                $('.tags-search-panel').show();
                            }
                        })
                    }, 500);
                }
            }
        });
        $(document).click(function(e) {
            if (0 === $(e.target).parents(".tags-panel").length && 
                0 === $(e.target).parents(".editor-tags-box").length &&
                !$(e.target).hasClass(".editor-tags-box")) {
                $('.tags-panel').hide();
            }
        });

        function clearSearchAjax() {
            if (window.searchAjax !== null) {
                if (window.searchAjax.readystate !== 4) {
                    window.searchAjax.abort();
                }
                window.searchAjax = null;
            }
        }

        function clearSearchTimeout() {
            if (window.searchTimeout !== null) {
                clearTimeout(window.searchTimeout);
                window.searchTimeout = null;
            }
        }

        function insertTag(id, name) {
            if ($tags.find("option[value='" + id + "']").length === 0) {
                var option = new Option(name, id, false, false);
                $tags.append(option).trigger('change');
            }
            var val = $tags.val();
            if (val === null) {
                val = [id]
            } else if (val.indexOf(id) === -1 && val.length < 5) {
                val.push(id);
            }
            $tags.val(val).trigger('change');
            updateTagPanelLeft();
            $('.select2-search__field').val('');
            $('.tags-search-panel').hide();
            clearSearchAjax();
            clearSearchTimeout();
        }

        function showCreateTagModal(word) {
            $('.tags-panel').hide();
            $('.tags-search-panel').hide();
            $('.tag-form .tag-name').val(word);
            $('.tag-form .tag-desc').val('');
            $('#create-tag-modal').modal('show');
            $('.select2-search__field').val('');
            clearSearchAjax();
            clearSearchTimeout();
        }

        $('.tags-panel .tag').click(function () {
            insertTag($(this).data('id'), $(this).data('name'));
        });

        $(document).on('click', '.create-tag-item', function () {
            showCreateTagModal($(this).data('name'));
        });

        $(document).on('click', '.tag-item', function () {
            insertTag($(this).data('id'), $(this).data('name'));
        });

        $('#create-tag-modal .tag-form').submit(function () {
            var $btn = $(this).find('.btn-submit');
            $btn.button('loading');
            $(this).ajaxSubmit({
                success: function (data) {
                    $btn.button('reset');
                    if (data.code === 0) {
                        insertTag(data.id, data.name);
                        $('#create-tag-modal').modal('hide');
                    } else {
                        $('#alert-tmpl').tmpl(data).prependTo('#create-tag-modal .modal-body');
                    }
                }
            })
            return false;
        });

        $('.editor-form').submit(function　() {
            var id = $(this).data('qid');
            var title = $(this).find('#title').val();
            var tags = $tags.val();
            var content = $(this).find('#wmd-inputmarkdown').val();
            if (!title) {
                window.$K.error('标题不能为空！');
            } else if (!tags) {
                window.$K.error('标签不能为空！');
            } else if (content.length　< 20) {
                window.$K.error('正文不能少于20个字符！');
            } else {
                $(this).find('.btn-submit').button('loading');
                $.ajax({
                    url: "/questions/post",  
                    data: {
                        id: id,
                        title: title,
                        tags: tags,
                        content: content
                    },
                    type: 'post',  
                    dataType: 'json',  
                    success: function (data) {
                        $(this).find('.btn-submit').button('reset');
                        if (data.code === 0) {
                            window.location.href = data.next;
                        } else {
                            window.$K.error(data.msg);
                        }
                    }
                })
            }
            return false;
        });

        $('.answer-form').submit(function　() {
            var qid = $(this).data('qid');
            var aid = $(this).data('aid');
            var content = $(this).find('#wmd-inputmarkdown').val();
            if (content.length　< 10) {
                window.$K.error('正文不能少于10个字符！');
            } else {
                $(this).find('.btn-submit').button('loading');
                $.ajax({
                    url: "/questions/" + qid + "/answer",  
                    data: {
                        id: aid,
                        content: content
                    },
                    type: 'post',  
                    dataType: 'json',  
                    success: function (data) {
                        $(this).find('.btn-submit').button('reset');
                        if (data.code === 0) {
                            window.location.href = data.next;
                        } else {
                            window.$K.error(data.msg);
                        }
                    }
                })
            }
            return false;
        });

        $('#image-file').change(function () {
            var name = $('#image-file').val();
            if (name) {
                $('#btn-image span').text('上传中');
                $('#btn-image, #input-insert-image').attr('disabled', 'disabled');
                $('#input-insert-image').val(name);
                $('#image-file').hide();
                $('#image-form').ajaxSubmit({
                    success: function (data) {
                        if (data.code === 0) {
                            $('#input-insert-image').val(data.url);
                        } else {
                            window.alert(data.msg);
                        }
                        $('#btn-image span').text('选择图片');
                        $('#btn-image').removeAttr('disabled');
                        $('#image-file').show();
                    },
                    error: function (data) {
                        window.alert('上传失败！');
                        $('#btn-image span').text('选择图片');
                        $('#btn-image').removeAttr('disabled');
                        $('#image-file').show();
                    }
                })
            }
        });
    });
} (jQuery);
