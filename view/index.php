<!DOCTYPE html>
<html lang="en">

<?php
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "plates";
    
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $stmt = $conn->prepare("SELECT * FROM plates ORDER BY `date` DESC, `time` DESC LIMIT 1");
    $stmt->execute();
    $plates = $stmt->fetch();

    // var_dump($plates)
    
    $car_image = $plates['car']; 
    $plate_image = $plates['image']; 
    $date = $plates['date'];
    $time = $plates['time'];
    $plate = $plates['plate'];


    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    $stmt = $conn->prepare("SELECT * FROM plates ORDER BY `date` DESC, `time` DESC");
    $stmt->execute();
    $verifyplates = $stmt->fetchAll();
    
?>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="css/style.css">
    <link rel="stylesheet" href="https://www.w3schools.com/w3css/4/w3.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <title>تشخیص پلاک</title>
</head>
<body>
<script> 
$(document).ready(function(){
setInterval(function(){
    $("#container").load(window.location.href + " #container" );
    $("#plates").load(window.location.href + " #plates" );
}, 1000);
});
function reload(){
    return window.location.reload();
}
</script>
<div class="container" id="container">
    <h2 class="section-title">پلاک جاری</h2>
    <div class="car-image">
        <img src="<?php echo($car_image); ?>" alt="تصویر ماشین">
    </div>
    <div class="plate-details">
        <img src="<?php echo($plate_image); ?>" alt="تصویر پلاک">
        <p><?php echo($plate); ?></p>
        <p>تاریخ: <?php echo($date); ?></p>
        <p>ساعت: <?php echo($time); ?></p>
        <div class="button-container">
            <button onclick="saveToDatabase()">ثبت و پردازش پلاک جدید</button>
            <!-- <button onclick="reload()" style="background-color: blue;">بازیابی تصویر جاری</button> -->
        </div>
    </div>
</div>
<h2 class="section-title">پلاک های ثبت شده</h2>
<table id='plates'>
    <tr>
        <th>عملیات</th>
        <th>تصویر پلاک</th>
        <th>پلاک</th>
        <th>تاریخ</th>
        <th>زمان</th>
    </tr>
    <?php foreach($verifyplates as $verifyplate) { ?>
    <tr>
        <td class="action-buttons">
            <button class="edit-btn" onclick="editRecord('<?php echo $verifyplate['id']; ?>')"><i class="fa fa-file"></i></button>
            <button class="delete-btn" onclick="deleteRecord('<?php echo $verifyplate['id']; ?>')"><i class="fa fa-trash"></i></button>
        </td>
        <td><img src="<?php echo($verifyplate['image']); ?>" alt="تصویر پلاک تایید شده"></td>
        <td><?php echo($verifyplate['plate']); ?></td>
        <td><?php echo($verifyplate['date']); ?></td>
        <td><?php echo($verifyplate['time']); ?></td>
    </tr>
    <?php } ?>
</table>

<script>
    function saveToDatabase() {
        var formData = new FormData();
        formData.append('status', 1);

        var xhr = new XMLHttpRequest();
        xhr.open("POST", "verify.php", true);
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4 && xhr.status === 200) {
                // window.location.reload();
            }
        };
        xhr.send(formData);
    }
</script>
</body>
</html>
