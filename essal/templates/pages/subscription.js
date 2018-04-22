

var url = window.location.href;
var package = url.split('package=')[1];
//$('[name="package"]').src("https://subscriptions.zoho.com/subscribe/fee1a467cf416b4201b1342967d005e36a2bba0f6b053217afe8ded60e8a6aa6/" + package);
document.getElementById('subscription').src = "https://subscriptions.zoho.com/subscribe/fee1a467cf416b4201b1342967d005e36a2bba0f6b053217afe8ded60e8a6aa6/" + package;
