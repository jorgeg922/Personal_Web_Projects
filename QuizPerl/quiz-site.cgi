#!/usr/bin/perl
use DBI;
use CGI ':standard';


$register=param('register');
$login=param('login');
$rankings=param('rankings');
$submitquiz=param('submitquiz');
$checkscore=param('checkscore');
$dbh = DBI->connect("DBI:mysql:username","username",'password');

print "Content-type: text\html\n\n";

print "<html>
		<head>
			<title>Quiz - Project</title>
		<style>
			.intro{text-align:center;}
			.main{text-align:center;}
			.logindiv{text-align:center;}
		</style>
		<script>
			function myValidation(){
			var numPresident = -1;
			var numSpeaker = -1;
			var numVicep = -1;
			var numGovernor = -1;
			var numEcon = -1;

			for(i=0; i<quizform.president.length; i++){
				if(quizform.president[i].checked){
					numPresident = i;
				}
			}
			if(numPresident == -1){ alert('Pick a President');return false;}
			
			for(i=0; i<quizform.speaker.length; i++){
                                if(quizform.speaker[i].checked){
                                        numSpeaker = i;
                                }
                        }
                        if(numSpeaker == -1){ alert('Pick a Speaker');return false;}
		
			for(i=0; i<quizform.vicep.length; i++){
                                if(quizform.vicep[i].checked){
                                        numVicep = i;
                                }
                        }
                        if(numVicep == -1){ alert('Pick a Vice-President');return false;}	
			
			for(i=0; i<quizform.governor.length; i++){
                                if(quizform.governor[i].checked){
                                        numGovernor = i;
                                }
                        }
                        if(numGovernor == -1){ alert('Pick a Governor');return false;}

			for(i=0; i<quizform.econ.length; i++){
                                if(quizform.econ[i].checked){
                                        numEcon = i;
                                }
                        }
                        if(numEcon == -1){ alert('Pick a State');return false;}
			return true;
			}
		</script>
		</head>
		<body style='width:85%; margin:auto; border:2px solid red;'>";

print "<div class='intro'><h1>Welcome to Jorge Gonzales' semester Project!</h1>
		<p>If you are new please register. Otherwise log in to take the quiz or check your score</p>
		<p>Note: You are only allowed to take the quiz once, so think carefully about your answers!</p>
		<a href='quiz.cgi?register=yes'><button style='width:30%;'>First Time User</button></a>
		<a href='quiz.cgi?login=yes'><button style='width:30%;'>Login</button></a>
		<a href='quiz.cgi?rankings=yes'><button style='width:30%;'>Top 15 Scores</button></a></div>";
if($register){
print "<form class='main' method='get' action='quiz.cgi' style='margin-top:5%;'>
		First Name:<input type='text' name='fname' placeholder='First Name' required>	
		Last Name:<input type='text' name='lname' placeholder='Last Name' required>
		<br>
		<br>
		Create Password:<input type=text name='password' placeholder='Password' required>
		<br><br>
		<input type='submit' value='Register' name='registeruser'>	
	</form>";
}

$registeruser = param('registeruser');
if($registeruser){
$fname=param('fname');
$lname=param('lname');
$password=param('password');
	if($fname ne '' && $lname ne '' && $password ne ''){
		$queryCheck = $dbh ->prepare("select * from quiz where fname='$fname' and lname='$lname'");
		$queryCheck -> execute;
		$numcheck = $queryCheck -> rows;
		if($numcheck == 0){
			$queryRegister = $dbh -> prepare("insert into quiz values('', '$fname', '$lname', '$password', '', '', '', '')");
			$queryRegister -> execute;
			print"<p style='text-align:center;'>$fname has been added. Please <a href=quiz.cgi?login=yes>log in</a></p>"
		}else{print"<p style='text-align:center;>User $fname $lname already exists. Plese <a href=quiz.cgi?login=yes>log in</a></p>"}
	}
	
}

if($login){
print "<form class='logindiv' method='get' action='quiz.cgi' style='margin-top:5%;'>
		<h2>Enter your credentials:</h2>
		<br>
		First Name:<input type='text' name='fname' placeholder='First Name' required>	
		Last Name:<input type='text' name='lname' placeholder='Last Name' required>	
		<br>
		<br>
		Password:<input type='password' name='password' placeholder='Password' required>
		<br><br>
		<input type='submit' value='Login' name='loginuser'>
	</form>";
}

$loginuser=param('loginuser');
$fname=param('fname');
$lname=param('lname');
$password=param('password');
if($loginuser){
	$querylogin = $dbh->prepare("select *  from quiz where fname='$fname' and lname='$lname' and password='$password'");
	$querylogin->execute;

	@row = $querylogin->fetchrow_array;
		($id, $fname, $lname, $password, $dateoftest, $timeoftest, $score, $testtaken)=(@row);
	#print"<p>$id $fname $lname $password $dateiftest $timeoftest $score $testtaken</p>";
	if($id eq ''){
		print "<p style='text-align:center;'>Your information does not match our records. Try again</p>";
		last;
	}

	if($testtaken > 0){
		print "<p style='text-align:center;'>You already took the quiz!</p>";
		print"<p style='text-align:center;'><a href='quiz.cgi?checkscore=$id'><button>Check Score</button></a></p>";
		last;
	}

	print "<div class='wrapper' style='border:2px solid blue;'>
		<form method='get' name='quizform' action='quiz.cgi' onsubmit='return myValidation(this)'>
			<input type='hidden' name='userID' value='$id'>
			<p>1.Who is the current president of the U.S?<br>
				<input type='radio' name='president' value='obama'>Barack Obama<br>
				<input type='radio' name='president' value='lincoln'>Abraham Lincoln<br>
				<input type='radio' name='president' value='trump'>Donald Trump<br>
			</p>
			<p>2.Who is the current speaker of the House of Representatives?<br>
				<input type='radio' name='speaker' value='ryan'>Paul Ryan<br>
				<input type='radio' name='speaker' value='pelosi'>Nancy Pelosi<br>
				<input type='radio' name='speaker' value='schumer'>Chuck Schumer<br>
			</p>
			<p>3.Who was the previous vice president?<br>
				<input type='radio' name='vicep' value='bush'>George Bush<br>
				<input type='radio' name='vicep' value='flake'>Jeff Flake<br>
				<input type='radio' name='vicep' value='biden'>Joe Biden<br>
			</p>4.Who is the Governor of California?<br>
				<input type='radio' name='governor' value='washington'>George Washington<br>
                                <input type='radio' name='governor' value='brown'>Jerry Brown<br>
                                <input type='radio' name='governor' value='shawn'>Kelly Shawn<br>
			</p>
			<p>5.What state is the 5th largest economy of the world?<br>
				<input type='radio' name='econ' value='california'>California<br>
                                <input type='radio' name='econ' value='york'>New York<br>
                                <input type='radio' name='econ' value='alabama'>Alabama<br>
			</p>
			<input type='submit' name='submitquiz' value='Submit'>			
		</form></div>";
}

if($submitquiz){
$president=param('president');
$speaker=param('speaker');
$vicep=param('vicep');
$governor=param('governor');
$econ=param('econ');
$id=param('userID');
	if($president eq "trump"){
		$counter = $counter + 1;
	}
	if($speaker eq "ryan"){
                $counter = $counter + 1;
        }
	if($vicep eq "biden"){
		$counter = $counter + 1;
	}
	if($governor eq "brown"){
		$counter = $counter + 1;
	}
	if($econ eq "california"){
		$counter = $counter + 1;
	}

print"<h2 style=text-align:center;>Your score: $counter out of 5</h2>";
$queryscore = $dbh->prepare("update quiz set score=$counter,dateoftest=CURRENT_DATE, timeoftest=CURRENT_TIME, testtaken=1 where id='$id' ");
$queryscore->execute;
}

if($checkscore){

	$queryscoreget = $dbh->prepare("select score from quiz where id='$checkscore'");
	$queryscoreget->execute;
	@row = $queryscoreget->fetchrow_array;
                ($score)=(@row);
	print "<p style='text-align:center;'>Your score: $score out of 5";
}

if($rankings){
	$queryranks = $dbh->prepare("select fname, lname, score from quiz order by score desc limit 15");
	$queryranks->execute;
	print "<br><br><table border='1' style='margin:auto;'><tr>
		<th>First Name</th>
		<th>Last Name</th>
		<th>Score</th>
		</tr>";

	while(@row = $queryranks->fetchrow_array){
		($fname, $lname, $score) = (@row);
		
		print "<tr>
			<td>$fname</td>
			<td>$lname</td>
			<td>$score</td>
			</tr>";
	}

	print "</table>";
}

print "</body></html>";
