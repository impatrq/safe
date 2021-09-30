import 'package:get/get.dart' hide Worker;
import 'package:flutter/material.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/services/nfc_reader.dart';
import 'package:safe_app/components/customWidgets/worker_description_sheet.dart';
import 'package:safe_app/services/safe_api_helper.dart';
import 'package:safe_app/models/worker.dart';

class FinderController extends GetxController {

  final SAFEApiHelper _safeApiHelper = SAFEApiHelper();

  void _startSession(){
    NFCReader.startSession((code) async {

      var res = await _safeApiHelper.searchWorkerByCard(code);

      try
      {
        Worker worker = res;
        await Get.bottomSheet(
          WorkerDescriptionSheet(
            imageURL: worker.imagePath,
            name: '${worker.firstName} ${worker.lastName}',
            email: worker.email,
            address: worker.address,
            phoneNumber: worker.phoneNumber,
          ),
        );
      }
      catch(e)
      {
        Get.snackbar(
          'Error:',
          res,
          colorText: Colors.white,
          backgroundColor: kLogoDarkBlueColor.withOpacity(0.9),
          icon: Icon(FontAwesomeIcons.timesCircle, color: Colors.white,),
          margin: EdgeInsets.symmetric(vertical: 5.0, horizontal: 20.0),
        );
      }

      _startSession();

    });
  }

  void _stopSession() async {
    await NFCReader.stopSession();
  }

  @override
  void onInit() {
    super.onInit();
    _startSession();
  }

  @override
  void onClose() {
    super.onClose();
    _stopSession();
  }

}