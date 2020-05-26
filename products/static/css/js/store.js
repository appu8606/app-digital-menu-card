if (document.readyState == 'loading')
{
    document.addEventListener('DOMContentLoaded',ready)
}
else{
    ready()
}

function ready() {
var removeCartItemButtons = document.getElementsByClassName("btn-danger")
for (var i=0; i<removeCartItemButtons.length; i++)
{
    var button=removeCartItemButtons[i]
    button.addEventListener('click', removeCartItem)
}
} 
function removeCartItem(event){
    var buttonClicked = event.target
        buttonClicked.parentElement.parentElement.remove()
        updateCartTotal()
}

function updateCartTotal(){
    var cartrows = document.getElementsByClassName('cart-row')
    for(var i=0;i<cartrows.length;i++)
    {
        var cartrow=cartrows[i]
        var priceElement =cartrow.getElementsByClassName('cart-price')[0]

        var total=0
        var price=parseFloat(priceElement.innerText.replace('₹',''))
        total=total+price
    }
    document.getElementsByClassName('cart-total')[0].innerText = '₹' + total
}

