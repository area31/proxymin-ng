<?php include("./config.php");
include("../class.login.php");
$log = new logmein();
$log->encrypt = true;
if($log->logincheck($_SESSION['loggedin'], "logon", "password", "useremail") == false){
    //do something if NOT logged in. For example, redirect to login page or display message.
        header("Location: http://$_SERVER[HTTP_HOST]/auth.php?refer=$_SERVER[REQUEST_URI]");
}else{
    //do something else if logged in.
        header("Location: http://$_SERVER[HTTP_HOST]/proxymin/proxymin.py");
}
?>
