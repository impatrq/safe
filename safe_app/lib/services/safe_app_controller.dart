import 'package:get/get.dart';
import 'package:safe_app/utilities/data.dart';
import 'package:safe_app/services/safe_api_helper.dart';

class SafeAppController extends GetxController {

  final Data data = Data();
  final SAFEApiHelper _safeApiHelper = SAFEApiHelper();

  Future<void> initialize() async {
    await updateDoorsList();
    await updateLastLogsList();
    await updateWorkersList();
  }

  Future<void> updateDoorsList() async {
    var doorsList = await _safeApiHelper.getDoors();
    data.doorsList = doorsList;
    update();
  }

  Future<void> updateLastLogsList() async {
    var lastLogs = await _safeApiHelper.getLastLogs();
    data.lastLogsList = lastLogs;
    update();
  }

  Future<void> updateWorkersList() async {
    var workersList = await _safeApiHelper.getWorkers();
    data.workersList = workersList;
    update();
  }
  
  Future<void> searchWorker(String searchQuery) async {
    var workersList = await _safeApiHelper.searchWorker(searchQuery);
    data.workersList = workersList;
    update();
  }

  Future<void> searchDoor(String searchQuery) async {
    var doorsList = await _safeApiHelper.searchDoor(searchQuery);
    data.doorsList = doorsList;
    update();
  }

}