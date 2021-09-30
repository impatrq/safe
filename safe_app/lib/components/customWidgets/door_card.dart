import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/screens/door_details_screen.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class DoorCard extends StatelessWidget {

  DoorCard({required this.name, required this.isOpened, required this.sanitizer, required this.onTap, required this.isSafe, required this.peopleInside, required this.logs});

  final String name;
  final bool isOpened;
  final bool isSafe;
  final String sanitizer;
  final int peopleInside;
  final logs;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => Get.to(() => DoorDetailsScreen(doorName: name, peopleInside: peopleInside, sanitizer: sanitizer, isOpened: isOpened, isSafe: isSafe, logs: logs)),
      child: Row(
        children: [
          Container(
            width: MediaQuery.of(context).size.width * 0.8,
            height: 190.0,
            child: Card(
              color: Color(0xFFEFEFEF),
              elevation: 5.0,
              shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10.0)
              ),
              child: Padding(
                padding: EdgeInsets.all(16.0),
                child: Row(
                  children: [
                    Expanded(
                      flex: 2,
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Text(
                            '$name',
                            style: kLittleGreyTextStyle.copyWith(fontWeight: FontWeight.bold),
                            textAlign: TextAlign.center,
                          ),
                          FittedBox(
                            fit: BoxFit.fitWidth,
                            child: Text(
                              isOpened ? 'Abierta' : 'Cerrada',
                              style: kBigTitleTextStyle.copyWith(fontSize: 30.0),
                              textAlign: TextAlign.center,
                            ),
                          ),
                          Card(
                            color: isSafe ? Colors.green : Colors.red,
                            child: Padding(
                              padding: EdgeInsets.symmetric(vertical: 4.0, horizontal: 10.0),
                              child: Text(
                                isSafe ? 'SEGURO' : 'NO SEGURO',
                                style: kButtonBoldWhiteTextStyle,
                                textAlign: TextAlign.center,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                    Expanded(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            isOpened ? FontAwesomeIcons.doorOpen : FontAwesomeIcons.doorClosed,
                            color: kLogoDarkBlueColor,
                            size: 60.0,
                          ),
                          SizedBox(height: 10.0,),
                          Text(
                            'Sanitizante: $sanitizer',
                            style: kLittleGreyTextStyle,
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
          SizedBox(width: 10.0,),
        ],
      ),
    );
  }
}