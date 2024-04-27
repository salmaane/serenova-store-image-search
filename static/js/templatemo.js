/*

TemplateMo 559 Zay Shop

https://templatemo.com/tm-559-zay-shop

*/

'use strict';
$(document).ready(function() {

    // Accordion
    var all_panels = $('.templatemo-accordion > li > ul').hide();

    $('.templatemo-accordion > li > a').click(function() {
        console.log('Hello world!');
        var target =  $(this).next();
        if(!target.hasClass('active')){
            all_panels.removeClass('active').slideUp();
            target.addClass('active').slideDown();
        }
      return false;
    });
    // End accordion

    // Product detail
    $('.product-links-wap a').click(function(){
      var this_src = $(this).children('img').attr('src');
      $('#product-detail').attr('src',this_src);
      return false;
    });
    $('#btn-minus').click(function(){
      var val = $("#var-value").html();
      val = (val=='1')?val:val-1;
      $("#var-value").html(val);
      $("#product-quanity").val(val);
      return false;
    });
    $('#btn-plus').click(function(){
      var val = $("#var-value").html();
      val++;
      $("#var-value").html(val);
      $("#product-quanity").val(val);
      return false;
    });
    $('.btn-size').click(function(){
      var this_val = $(this).html();
      $("#product-size").val(this_val);
      $(".btn-size").removeClass('btn-secondary');
      $(".btn-size").addClass('btn-success');
      $(this).removeClass('btn-success');
      $(this).addClass('btn-secondary');
      return false;
    });
    // End roduct detail

});

function previewImage() {
            var input = document.getElementById('image');
            var preview = document.getElementById('preview-image');
            var container = document.getElementById('preview-image-container');

            if (input.files && input.files[0]) {
                var reader = new FileReader();

                reader.onload = function (e) {
                    const resultContainer = document.getElementById('resultContainer');
                    resultContainer.innerHTML = '';
                    preview.src = e.target.result;
                    container.classList.remove("d-none");
                };

                reader.readAsDataURL(input.files[0]);
            }
        }

function searchProducts() {
    const input = document.getElementById('image');
    const spinner = document.getElementById('spinner');
    const file = input.files[0];

    if (file) {
        const formData = new FormData();
        formData.append('image', file);
        spinner.hidden = false;

        fetch('/image-search', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            spinner.hidden = true;
            const resultContainer = document.getElementById('resultContainer');
            resultContainer.innerHTML='';
            if(data.length === 0) {
                resultContainer.innerHTML = `<h5 class="mt-3 text-center" style="color: #555">sorry no similar products found</h5>`;
            } else {
                resultContainer.innerHTML += `<h4 class="mt-2" style="color: #444">search results:</h4>`
                for(let i=0; data.length; i++) {
                    let productHtml =  `
                        <div class="col-md-3">
                            <div class="card mb-4 product-wap rounded-0 overflow-hidden" style="height: 480px">
                                <div class="card rounded-0">
                                    <img class="card-img rounded-0" src="/static/img/images/${data[i]['Image']}" alt="" style="max-height: 300px">
                                    <div class="card-img-overlay rounded-0 product-overlay d-flex align-items-center justify-content-center">
                                        <ul class="list-unstyled">
                                            <li><a class="btn btn-success text-white" href="/shop-single/${data[i]['ProductId']}"><i class="far fa-heart"></i></a></li>
                                            <li><a class="btn btn-success text-white mt-2" href="/shop-single/${data[i]['ProductId']}"><i class="far fa-eye"></i></a></li>
                                            <li><a class="btn btn-success text-white mt-2" href="/shop-single/${data[i]['ProductId']}"><i class="fas fa-cart-plus"></i></a></li>
                                        </ul>
                                    </div>
                                </div>
                                <div class="card-body">
                                    <a href="{{ url_for('shopSingle', pid=${data[i]['ProductId']} }}" class="h3 text-decoration-none">${data[i]['ProductTitle']}</a>
                                    <ul class="w-100 list-unstyled d-flex justify-content-between mb-0">
                                        <li>M/L/X/XL</li>
                                        <li class="pt-2">
                                            <span class="product-color-dot color-dot-red float-left rounded-circle ml-1"></span>
                                            <span class="product-color-dot color-dot-blue float-left rounded-circle ml-1"></span>
                                            <span class="product-color-dot color-dot-black float-left rounded-circle ml-1"></span>
                                            <span class="product-color-dot color-dot-light float-left rounded-circle ml-1"></span>
                                            <span class="product-color-dot color-dot-green float-left rounded-circle ml-1"></span>
                                        </li>
                                    </ul>
                                    <ul class="list-unstyled d-flex justify-content-center mb-1">
                                        <li>
                                            <i class="text-warning fa fa-star"></i>
                                            <i class="text-warning fa fa-star"></i>
                                            <i class="text-warning fa fa-star"></i>
                                            <i class="text-muted fa fa-star"></i>
                                            <i class="text-muted fa fa-star"></i>
                                        </li>
                                    </ul>
                                    <p class="text-center mb-0">$250.00</p>
                                </div>
                            </div>
                    `;
                    resultContainer.innerHTML += productHtml;
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}