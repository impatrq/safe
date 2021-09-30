import 'package:flutter/material.dart';
import 'package:safe_app/services/nfc_reader.dart';
import 'package:safe_app/utilities/constants.dart';

class NFCAvailableWidget extends StatefulWidget {

  NFCAvailableWidget({required this.availableWidget, this.blankResult = false});

  final Widget availableWidget;
  final bool blankResult;

  @override
  _NFCAvailableWidgetState createState() => _NFCAvailableWidgetState();
}

class _NFCAvailableWidgetState extends State<NFCAvailableWidget> {

  Widget currentWidget = Text('Tu dispositivo no cuenta con NFC / No está activado.', style: kLittleGreyTextStyle,);

  void checkAvailability() async {
    if(await NFCReader.checkAvailability()) {
      setState(() {
        this.currentWidget = widget.availableWidget;
      });
    } else if(widget.blankResult == true){
        setState(() {
          this.currentWidget = SizedBox();
        });
    }
  }

  @override
  void initState() {
    super.initState();
    checkAvailability();
  }

  @override
  Widget build(BuildContext context) {
    return currentWidget;
  }
}