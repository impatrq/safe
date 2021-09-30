import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/components/scaffolding/back_arrow_scaffold.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/services/finder_controller.dart';

class FinderScreen extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return GetBuilder<FinderController>(
      init: FinderController(),
      builder: (finderController) => BackArrowScaffold(
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Icon(
                FontAwesomeIcons.idCardAlt,
                color: kLogoDarkBlueColor,
                size: 100.0,
              ),
              SizedBox(height: 50.0,),
              Text(
                'Apoye una tarjeta en la parte posterior del dispositivo.',
                // 'Su dispositivo no cuenta con lector NFC.',
                style: TextStyle(
                  color: Colors.grey.shade500,
                  fontFamily: 'Nunito',
                  fontSize: 30.0,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
