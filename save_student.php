<?php
// Simple form handler for RecruitCSRams student registration

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    die('Invalid request method.');
}

$full_name = isset($_POST['full_name']) ? trim($_POST['full_name']) : '';
$email     = isset($_POST['email']) ? trim($_POST['email']) : '';
$school    = isset($_POST['school']) ? trim($_POST['school']) : '';
$grade     = isset($_POST['grade']) ? trim($_POST['grade']) : '';
$attending = isset($_POST['attending']) ? $_POST['attending'] : '';
$interests = isset($_POST['interests']) ? $_POST['interests'] : [];

$errors = [];

if ($full_name === '') {
    $errors[] = 'Full name is required.';
}
if ($email === '') {
    $errors[] = 'Email is required.';
}
if ($attending === '') {
    $errors[] = 'Please select if you will attend the Open House.';
}

if (!empty($errors)) {
    echo "<h2>There were some problems with your submission:</h2>";
    echo "<ul>";
    foreach ($errors as $e) {
        echo "<li>" . htmlspecialchars($e) . "</li>";
    }
    echo "</ul>";
    echo '<p><a href="student_register.html">Go back to the registration form</a></p>';
    exit;
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Registration Confirmed</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
        }
        .container {
            max-width: 600px;
            margin: 40px auto;
            background: #ffffff;
            padding: 20px 30px;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 {
            color: #0066cc;
        }
        p {
            line-height: 1.5;
        }
        .label {
            font-weight: bold;
        }
    </style>
</head>
<body>
<div class="container">
    <h1>Thank You for Registering!</h1>
    <p>Your information has been received for the Computer Science Open House.</p>

    <p><span class="label">Name:</span> <?php echo htmlspecialchars($full_name); ?></p>
    <p><span class="label">Email:</span> <?php echo htmlspecialchars($email); ?></p>
    <p><span class="label">High School:</span> <?php echo htmlspecialchars($school); ?></p>
    <p><span class="label">Grade:</span> <?php echo htmlspecialchars($grade); ?></p>
    <p><span class="label">Attending:</span> <?php echo htmlspecialchars($attending); ?></p>

    <p><span class="label">Interests:</span>
        <?php
        if (count($interests) === 0) {
            echo "None selected";
        } else {
            echo htmlspecialchars(implode(', ', $interests));
        }
        ?>
    </p>

    <p>Later, this page can show your QR code and personalized schedule.</p>
</div>
</body>
</html>
