import 'package:flutter/cupertino.dart';
import 'package:nfc_manager/nfc_manager.dart';

class NFCReader {

  static Future<bool> checkAvailability() async {
    // Check availability
    return await NfcManager.instance.isAvailable();
  }

  static void startSession(Function(String) callback){
    // Start Session
    NfcManager.instance.startSession(
      onDiscovered: (NfcTag tag) async {
        await stopSession();
        callback(tag.data['nfca']['identifier'].join(''));
      },
    );
    print('NFC Reading Session Started');
  }

  static Future<void> stopSession() async {
    // Stop Session
    await NfcManager.instance.stopSession();
    print('NFC Reading Session Stopped');
  }

}