import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:safe_app/screens/door_details_screen.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class DoorListTile extends StatelessWidget {

  DoorListTile({required this.name, required this.peopleInside, required this.sanitizer, required this.isOpened, required this.isSafe, required this.logs});

  final String name;
  final int peopleInside;
  final String sanitizer;
  final bool isOpened;
  final bool isSafe;
  final logs;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => Get.to(() => DoorDetailsScreen(doorName: name, peopleInside: peopleInside, sanitizer: sanitizer, isOpened: isOpened, isSafe: isSafe, logs: logs)),
      child: Column(
        children: [
          SizedBox(height: 10.0,),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              Expanded(
                flex: 2,
                child: Text(
                  name,
                  style: kLittleTitleTextStyle.copyWith(fontSize: 14.0),
                  textAlign: TextAlign.center,
                ),
              ),
              Expanded(
                child: Text(
                  sanitizer,
                  style: kLittleTitleTextStyle.copyWith(fontSize: 14.0),
                  textAlign: TextAlign.center,
                ),
              ),
              Expanded(
                child: Icon(
                  isSafe ? FontAwesomeIcons.checkCircle : FontAwesomeIcons.timesCircle,
                  color: isSafe ? Colors.green : Colors.red,
                ),
              )
            ],
          ),
          SizedBox(height: 10.0,),
          Divider(thickness: 1,),
        ],
      ),
    );
  }
}