import 'package:get/get.dart';
import 'package:shared_preferences/shared_preferences.dart';

class AuthController extends GetxController {

  Future<void> saveUserData(int id, String name, String email) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setInt('userId', id);
    prefs.setString('userName', name);
    prefs.setString('userEmail', email);
  }

  Future<dynamic> getLoggedInUserData() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    int? id = prefs.getInt('userId');
    String? name = prefs.getString('userName');
    String initials = '${name.toString().split(' ')[0][0]} ${name.toString().split(' ')[1][0]}';
    String? email = prefs.getString('userEmail');
    return {
      'id': id,
      'name': name,
      'initials': initials,
      'email': email
    };
  }

  Future<bool> checkIfLoggedIn() async {

    SharedPreferences prefs = await SharedPreferences.getInstance();

    int? loggedInUserId = prefs.getInt('loggedInUserId');

    if(loggedInUserId != -1 && loggedInUserId != null){
      return true;
    } else {
      return false;
    }
  }

  Future<void> loginUser(int id) async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setInt('loggedInUserId', id);
    print('User with id $id logged in');
  }

  Future<void> logoutUser() async {
    SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setInt('loggedInUserId', -1);
    print('User logged out');
  }


}