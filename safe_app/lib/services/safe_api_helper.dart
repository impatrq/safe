import 'dart:convert';
import 'package:get/get.dart' hide FormData, Worker, MultipartFile;
import 'package:dio/dio.dart';
import 'package:safe_app/models/door.dart';
import 'package:safe_app/models/log.dart';
import 'package:safe_app/models/worker.dart';
import 'package:safe_app/services/auth_controller.dart';

class SAFEApiHelper {

  final AuthController _authController = AuthController();

  final Dio _dio = Dio();

  final String _secretKey = 'qlswpZD6rvyCxkd4jrAkZf2gf5pWI5zn';
  final String _host = 'http://safe.com.ar';

  Future<dynamic> login(String identifier, String password, bool? keepLoggedIn) async {

    try
    {
      var formData = FormData.fromMap({
        'SECRET_KEY': _secretKey,
        'identifier': identifier,
        'password': password,
      });

      var response = await _dio.post('$_host/api/auth/login/', data: formData);

      if(response.data['authorized'] == 'true'){
        if(keepLoggedIn == true){
          await _authController.loginUser(response.data['user_id']);
        }
        await _authController.saveUserData(response.data['user_id'], response.data['user']['name'], response.data['user']['email']);
        return;
      } else {
        return response.data['error_message'];
      }
    } catch(e)
    {
      print(e.toString());
      return 'An unexpected error occurred, try again.';
    }

  }

  Future<dynamic> getDoors() async {

    try
    {

      var userData = await _authController.getLoggedInUserData();
      int userId = userData['id'];

      var response = await _dio.get('$_host/api/tables/doors/get_doors_status?sk=$_secretKey&user_id=$userId');

      var doors = jsonDecode(response.data['data']);

      List<Door> doorsList = [];

      doors.keys.forEach((doorKey){
        var doorData = doors[doorKey];

        List<Log> lastLogsList = [];

        jsonDecode(doorData['logs']).forEach((log){
          Log logItem = Log(workerName: log['worker_full_name'], workerEmail: log['worker_email'], workerAddress: log['worker_address'], workerPhoneNumber: log['worker_phone_number'], doorName: log['door_name'], entryDatetime: log['entry_datetime'], exitDatetime: log['exit_datetime'], faceMask: log['facemask'], temperature: log['temperature'], authorized: log['authorized'], workerLogImage: '${log['worker_image']}', workerProfileImage: log['worker_profile_image']);
          lastLogsList.add(logItem);
        });

        Door door = Door(
          doorName: doorData['door_name'],
          isOpened: doorData['is_opened'],
          peopleInside: jsonDecode(doorData['people_inside']).length,
          sanitizer: doorData['sanitizer_perc'],
          isSafe: doorData['is_safe'],
          logs: lastLogsList,
        );
        doorsList.add(door);
      });

      return doorsList;

    } catch(e)
    {
      print(e.toString());
      return 'An unexpected error occurred, try again.';
    }

  }

  Future<dynamic> getWorkers() async {

    try
    {
      var userData = await _authController.getLoggedInUserData();
      int userId = userData['id'];

      var response = await _dio.get('$_host/api/tables/workers/all?sk=$_secretKey&user_id=$userId');

      var workers = jsonDecode(response.data['data']);

      List<Worker> workersList = [];

      workers.forEach((worker){
        var workerData = worker['fields'];
        Worker workerItem = Worker(firstName: workerData['first_name'], lastName: workerData['last_name'], phoneNumber: workerData['phone_number'], email: workerData['email'], address: workerData['address'], cardCode: workerData['card_code'], imagePath: '$_host/media/${workerData['worker_image']}');
        workersList.add(workerItem);
      });

      return workersList;

    }
    catch(e)
    {
      print(e.toString());
      return 'An unexpected error occurred.';
    }

  }

  Future<dynamic> getLastLogs() async {

    try
    {
      var userData = await _authController.getLoggedInUserData();
      int userId = userData['id'];
      
      var response = await _dio.get('$_host/api/tables/logs?sk=$_secretKey&user_id=$userId');

      var logs = jsonDecode(response.data['data']['results']);

      List<Log> lastLogsList = [];

      logs.forEach((log){
        Log logItem = Log(workerName: log['worker_full_name'], workerEmail: log['worker_email'], workerAddress: log['worker_address'], workerPhoneNumber: log['worker_phone_number'], doorName: log['door_name'], entryDatetime: log['entry_datetime'], exitDatetime: log['exit_datetime'], faceMask: log['facemask'], temperature: log['temperature'], authorized: log['authorized'], workerLogImage: '$_host${log['worker_image']}', workerProfileImage: log['worker_profile_image']);
        lastLogsList.add(logItem);
      });

      return lastLogsList;

    }
    catch (e)
    {
      print(e.toString());
      return 'An unexpected error occurred.';
    }

  }

  Future<dynamic> addWorker(String firstName, String lastName, String phoneNumber, String email, String address, String cardCode, String imagePath) async {

    try
    {

      var userData = await _authController.getLoggedInUserData();
      int userId = userData['id'];

      var formData = FormData.fromMap({
        'SECRET_KEY': _secretKey,
        'user_id': userId,
        'first_name': firstName,
        'last_name': lastName,
        'phone_number': phoneNumber,
        'email': email,
        'address': address,
        'card_code': cardCode,
        'worker_image': await MultipartFile.fromFile(imagePath, filename: imagePath.split('/').last),
      });

      var response = await _dio.post('$_host/api/tables/workers/create/', data: formData);

      if(response.data['error_message'] != null){
        return response.data['error_message'];
      }

    } catch(e)
    {
      print(e.toString());
      return 'An unexpected error occurred, try again.';
    }

  }

  Future<dynamic> addDoor(String mac, String doorSector, String doorName, String sanitizer) async {

    try
    {
      var userData = await _authController.getLoggedInUserData();
      int userId = userData['id'];

      var formData = FormData.fromMap({
        'SECRET_KEY': _secretKey,
        'user_id': userId,
        'mac': mac,
        'sector_name': doorSector,
        'door_name': doorName,
        'sanitizer_perc': sanitizer,
      });

      var response = await _dio.post('$_host/api/tables/doors/create/', data: formData);

      if(response.data['error_message'] != null){
        return response.data['error_message'];
      }

    }
    catch(e)
    {
      print(e.toString());
      return 'An unexpected error occurred, try again.';
    }

  }

  Future<dynamic> searchWorker(String searchQuery) async {

    try
    {

      var userData = await _authController.getLoggedInUserData();
      int userId = userData['id'];

      String firstWord = '';
      String secondWord = '';

      try
      {
        firstWord =  searchQuery.split(' ')[0];
        secondWord = searchQuery.split(' ')[1];
      } catch(e) { }

      // print('Fetching to: $_host/api/tables/workers/search?sk=$_secretKey&user_id=$userId${firstWord != '' ? '&first_word=$firstWord':''}${secondWord != '' ? '&second_word=$secondWord':''}');
      var response = await _dio.get('$_host/api/tables/workers/search?sk=$_secretKey&user_id=$userId${firstWord != '' ? '&first_word=$firstWord':''}${secondWord != '' ? '&second_word=$secondWord':''}');

      var workers = jsonDecode(response.data['data']['results']);

      List<Worker> workersList = [];

      workers.forEach((worker){
        var workerData = worker['fields'];
        Worker workerItem = Worker(firstName: workerData['first_name'], lastName: workerData['last_name'], phoneNumber: workerData['phone_number'], email: workerData['email'], address: workerData['address'], cardCode: workerData['card_code'], imagePath: '$_host/media/${workerData['worker_image']}');
        workersList.add(workerItem);
      });

      return workersList;

    }
    catch(e)
    {
      print(e.toString());
      return 'An unexpected error occurred, try again.';
    }

  }

  Future<dynamic> searchWorkerByCard(String cardCode) async {

    try
    {

      var userData = await _authController.getLoggedInUserData();
      int userId = userData['id'];
      
      var response = await _dio.get('$_host/api/tables/workers/searchByCard?sk=$_secretKey&user_id=$userId&card_code=$cardCode');

      if(response.data['data'] != null){
        var workerData = jsonDecode(response.data['data'])[0]['fields'];

        Worker worker = Worker(
          firstName: workerData['first_name'],
          lastName: workerData['last_name'],
          phoneNumber: workerData['phone_number'],
          email: workerData['email'],
          address: workerData['address'],
          cardCode: workerData['card_code'],
          imagePath: '$_host/media/${workerData['worker_image']}',
        );

        return worker;

      } else {
        return response.data['error_message'];
      }

    }
    catch(e)
    {
      print(e.toString());
      return 'An unexpected error occurred.';
    }

  }

  Future<dynamic> searchDoor(String searchQuery) async {

    try
    {

      var userData = await _authController.getLoggedInUserData();
      int userId = userData['id'];

      String firstWord = '';
      String secondWord = '';

      try
      {
        firstWord =  searchQuery.split(' ')[0];
        secondWord = searchQuery.split(' ')[1];
      } catch(e) { }

      // print('Fetching to: $_host/api/tables/workers/search?sk=$_secretKey&user_id=$userId${firstWord != '' ? '&first_word=$firstWord':''}${secondWord != '' ? '&second_word=$secondWord':''}');
      var response = await _dio.get('$_host/api/tables/doors/search?sk=$_secretKey&user_id=$userId${firstWord != '' ? '&first_word=$firstWord':''}${secondWord != '' ? '&second_word=$secondWord':''}');

      var doors = jsonDecode(response.data['data']['complete_results']);

      List<Door> doorsList = [];

      doors.keys.forEach((doorKey){
        var doorData = doors[doorKey];

        List<Log> lastLogsList = [];

        jsonDecode(doorData['logs']).forEach((log){
          Log logItem = Log(workerName: log['worker_full_name'], workerEmail: log['worker_email'], workerAddress: log['worker_address'], workerPhoneNumber: log['worker_phone_number'], doorName: log['door_name'], entryDatetime: log['entry_datetime'], exitDatetime: log['exit_datetime'], faceMask: log['facemask'], temperature: log['temperature'], authorized: log['authorized'], workerLogImage: '${log['worker_image']}', workerProfileImage: log['worker_profile_image']);
          lastLogsList.add(logItem);
        });

        Door door = Door(
          doorName: doorData['door_name'],
          isOpened: doorData['is_opened'],
          peopleInside: jsonDecode(doorData['people_inside']).length,
          sanitizer: doorData['sanitizer_perc'],
          isSafe: doorData['is_safe'],
          logs: lastLogsList,
        );

        doorsList.add(door);

      });

      return doorsList;

    }
    catch(e)
    {
      print(e.toString());
      return 'An unexpected error occurred, try again.';
    }

  }

}