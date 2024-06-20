$(function () {
  // init feather icons
  feather.replace();

  // init tooltip & popovers
  $('[data-toggle="tooltip"]').tooltip();
  $('[data-toggle="popover"]').popover();

  //page scroll
  $("a.page-scroll").bind("click", function (event) {
    var $anchor = $(this);
    $("html, body")
      .stop()
      .animate(
        {
          scrollTop: $($anchor.attr("href")).offset().top - 20,
        },
        1000
      );
    event.preventDefault();
  });

  // slick slider
  $(".slick-about").slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    autoplay: true,
    autoplaySpeed: 3000,
    dots: true,
    arrows: false,
  });

  //toggle scroll menu
  var scrollTop = 0;
  $(window).scroll(function () {
    var scroll = $(window).scrollTop();
    //adjust menu background
    if (scroll > 80) {
      if (scroll > scrollTop) {
        $(".smart-scroll").addClass("scrolling").removeClass("up");
      } else {
        $(".smart-scroll").addClass("up");
      }
    } else {
      // remove if scroll = scrollTop
      $(".smart-scroll").removeClass("scrolling").removeClass("up");
    }

    scrollTop = scroll;

    // adjust scroll to top
    if (scroll >= 600) {
      $(".scroll-top").addClass("active");
    } else {
      $(".scroll-top").removeClass("active");
    }
    return false;
  });

  // scroll top top
  $(".scroll-top").click(function () {
    $("html, body").stop().animate(
      {
        scrollTop: 0,
      },
      1000
    );
  });

  /**Theme switcher - DEMO PURPOSE ONLY */
  $(".switcher-trigger").click(function () {
    $(".switcher-wrap").toggleClass("active");
  });
  $(".color-switcher ul li").click(function () {
    var color = $(this).attr("data-color");
    $("#theme-color").attr("href", "css/" + color + ".css");
    $(".color-switcher ul li").removeClass("active");
    $(this).addClass("active");
  });

  $(document).ready(function () {
    $("#picture-button").addClass("active");
    $("#picture-button, #camera-button").click(function () {
      $("#picture-button, #camera-button").removeClass("active");
      var newContentArea = document.getElementById("new-content-area");
      newContentArea.innerHTML = "";
      $("#picture-upload").val("");
      $(this).addClass("active");
      if ($(this).is("#picture-button")) {
        $("#picture-upload").show();
        $("#camera-stream-div2").hide();
        // $("#result-preview-text").text("Picture result preview");
        $("#convert-button").show();
        $("#result-table").show();
        $("#result-table2").hide();

        $("#picture-preview").hide();
        $("#enable-camera-button").hide();
        $("#detect-button").hide();
        $("#camera-stream").hide();
      } else if ($(this).is("#camera-button")) {
        $("#enable-camera-button").show();
        $("#detect-button").show();
        $("#picture-upload").hide();
        $("#result-table").hide();
        $("#result-cell").text("");
        $("#result-table2").show();
        // $("#result-preview-text").text("Real-time result preview");
        $("#convert-button").hide();
        $("#camera-stream-div2").show();
        $("#picture-preview").hide();
        $("#camera-stream").hide();
      }
    });
    $("#picture-button").click();
    $("#picture-preview").hide();
  });

  $("#enable-camera-button").click(function () {
    $("#camera-stream").show();
    $("#detect-button").show();
    $("#stop-button").hide();
  });

  $("#stop-button").click(function () {
    $("#detect-button").show();
    $("#stop-button").hide();
  });

  $("#detect-button").click(function () {
    $("#stop-button").show();
    $("#detect-button").hide();
  });

  $("#convert-button").click(function () {
    var formData = new FormData();

    if ($("#picture-upload")[0].files.length > 0) {
      formData.append("picture", $("#picture-upload")[0].files[0]);
      $("#result-cell").text("Processing...");
      // $("#picture-preview").show();

      $.ajax({
        type: "POST",
        url: "/process",
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
          var confidence_scores = data.confidence_scores;
          var class_names = data.class_names;

          $("#result-cell").text(class_names + " (" + confidence_scores + ")");
        },
      });
    } else {
      alert("Please upload a picture file.");
      return;
    }
  });

  var detectInterval;

  $("#detect-button").click(function () {
    detectInterval = setInterval(function () {
      updateCameraStream();
    }, 2000);

    $("#stop-button").show();
    $("#detect-button").hide();
  });

  $("#stop-button").click(function () {
    clearInterval(detectInterval);

    $("#stop-button").hide();
    $("#detect-button").show();
  });

  function updateCameraStream() {
    var cameraStreamSrc = $("#camera-stream").attr("src");
    $.ajax({
      type: "POST",
      url: "/test/vo",
      data: { camera_stream_src: cameraStreamSrc },
      success: function (data) {
        // 更新前端表格
        updateResultTable(data);
      },
    });
  }

  function updateResultTable(data) {
    if (data.position !== null && data.disease !== null) {
      var newRow = $("<tr>");
      newRow.append($("<td>").text(data.position));
      newRow.append($("<td>").text(data.disease));
      $("#result-table2").append(newRow);
    }
  }
});
