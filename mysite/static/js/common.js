var connFlag = false;
$(function(){
	//뉴스 다시 불러오기
	$('.btn-reload-data').on('click', function(){
		$('.loading').show();
	});

	//메뉴박스 열기
	$('.header .btn-gnb').on('click', function(){
		if(!connFlag){
			if($(this).hasClass('active')){
				$(this).removeClass('active');
				$('.gnb-box, .header .fncs').removeClass('show');
			}else{
				$(this).addClass('active');
				$('.gnb-box, .header .fncs').addClass('show');
			}
		}
	});

	//검색박스 열기
	$('.header .btn-open-search').on('click', function(){
		$('.search-box').addClass('show');
		$('.search-box input[type="text"]').focus();
	});
	$('.header .search-box .btn-close').on('click', function(){
		$('.search-box').removeClass('show');
		$('.search-box input[type="text"]').focusout();
	});

	//메뉴 이동
	$('.gnb-box .menu ul ul a').on('click', function(){
		$('.gnb-box .menu ul ul li').removeClass('active');
		$(this).parent('li').addClass('active');
	});
	$('.gnb-box .dim').on('click', function(){
		//close gnb box
		$('.header .btn-gnb').removeClass('active');
		$('.gnb-box, .header .fncs').removeClass('show');
	});

	//화면 테마 (light, dark)
	$('.view-mode-changer').on('change', function(){
		var skinMode = $(this).val();
		if(skinMode == 'dark'){
			$('#wrap').addClass('darkmode');
		}else{
			$('#wrap').removeClass('darkmode');
		}
	});
});

//Layer Content
function layerContShow(thisClass){
    $('.'+thisClass).show();
}
function layerContHide(thisClass){
    $('.'+thisClass).hide();
}
