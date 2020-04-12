$(function () {
  $('#deletebox').dialog({
    title: '글 삭제하기',
    autoOpen: false,
    dialogClass: 'no-close',
    show: {
        effect: 'scale',
        duration: 300
    },
    hide: {
        effect: 'scale',
        duration: 300
    },
    position: {
        my: 'bottom',
    },
    buttons: {
      '취소': function (e) {
          $('#deletebox').dialog('close');
      },
      '삭제': function (e) {
        $('#deleteform').submit();
      }
    },
    create: function () {
      $(this).closest(".ui-dialog").find(".ui-button").eq(1).addClass("cancel");
      $(this).closest(".ui-dialog").find(".ui-button").eq(2).addClass("admit")
      }
  });
  $('#deletebtn').button().click(function (e) {
    $('#deletebox').dialog('open');
  });
})

$(function () {
  $('#updatebox').dialog({
    title: '글 수정하기',
    autoOpen: false,
    dialogClass: 'no-close',
    show: {
        effect: 'scale',
        duration: 300
    },
    hide: {
        effect: 'scale',
        duration: 300
    },
    position: {
        my: 'bottom',
    },
    buttons: {
      '확인': function (e) {
        $('#updateform').submit();
      },
      '취소': function (e) {
          $('#updatebox').dialog('close');
      },
    },
    create: function () {
      $(this).closest(".ui-dialog").find(".ui-button").eq(1).addClass("admit");
      $(this).closest(".ui-dialog").find(".ui-button").eq(2).addClass("cancel")
      }
  });
  $('#updatebtn').button().click(function (e) {
    $('#updatebox').dialog('open');
  });
})