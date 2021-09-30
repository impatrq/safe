import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:qr_code_scanner/qr_code_scanner.dart';
import 'package:safe_app/services/icon_state_controller.dart';

class CustomQRView extends StatelessWidget {

  CustomQRView({required this.onRead});

  final Function(String) onRead;

  final GlobalKey qrKey = GlobalKey(debugLabel: 'QR');

  QRViewController? controller;

  void _onQRViewCreated(QRViewController controller) {
    this.controller = controller;
    controller.scannedDataStream.listen((scanData) {
        Get.back();
        onRead(scanData.code);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        QRView(
          key: qrKey,
          onQRViewCreated: _onQRViewCreated,
          overlay: QrScannerOverlayShape(
              borderColor: Colors.white,
              borderRadius: 20.0,
              borderLength: 20.0,
              borderWidth: 7.0,
              cutOutSize: 250.0,
          ),
        ),
        Align(
          alignment: Alignment.topRight,
          child: Padding(
            padding: EdgeInsets.all(8.0),
            child: GetBuilder<IconController>(
              init: IconController(),
              builder: (iconController) => IconButton(
                icon: Icon(
                  iconController.isFlashOn ? Icons.flash_off : Icons.flash_on,
                  color: Colors.white,
                  size: 30.0,
                ),
                onPressed: () async {
                  await controller?.toggleFlash();
                  iconController.toggleFlash();
                },
              ),
            ),
          ),
        ),
        Align(
          alignment: Alignment.topLeft,
          child: Padding(
            padding: EdgeInsets.all(8.0),
            child: IconButton(
              icon: Icon(
                FontAwesomeIcons.camera,
                color: Colors.white,
                size: 30.0,
              ),
              onPressed: () async {
                await controller?.flipCamera();
              },
            ),
          ),
        ),
      ],
    );
  }
}
