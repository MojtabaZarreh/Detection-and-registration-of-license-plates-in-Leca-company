<?php
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "plates";
    
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // if ($_SERVER["REQUEST_METHOD"] == "POST") {
    //     $plate = $_POST['plate'];
    //     $date = $_POST['date'];
    //     $time = $_POST['time'];
    //     $image = $_POST['image'];

    //     $stmt = $conn->prepare("INSERT INTO verifyplates (plate, date, time, image) VALUES (:plate, :date, :time, :image)");
    //     $stmt->bindParam(':plate', $plate);
    //     $stmt->bindParam(':date', $date);
    //     $stmt->bindParam(':time', $time);
    //     $stmt->bindParam(':image', $image);
    //     $stmt->execute();

    //     echo "اطلاعات با موفقیت ذخیره شد!";
    // } else {
    //     // اگر درخواست از نوع POST نبود
    //     echo "درخواست نامعتبر!";
    // }

    if ($_SERVER["REQUEST_METHOD"] == "POST") {
        $new_status = $_POST['status'];
        $sql = "UPDATE `status` SET `status` = $new_status WHERE id = 1";
        $stmt = $conn->prepare($sql);
        $stmt->execute();
    }
?>