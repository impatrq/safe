import 'dart:math';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:safe_app/components/scaffolding/back_arrow_scaffold.dart';
import 'package:safe_app/components/listTiles/door_log_tile.dart';
import 'package:safe_app/models/log.dart';
import 'package:safe_app/utilities/constants.dart';

class DoorDetailsScreen extends StatelessWidget {

  DoorDetailsScreen({required this.doorName, required this.peopleInside, required this.sanitizer, required this.isOpened, required this.isSafe, required this.logs});

  final String doorName;
  final int peopleInside;
  final String sanitizer;
  final bool isOpened;
  final bool isSafe;
  final List logs;

  @override
  Widget build(BuildContext context) {
    return BackArrowScaffold(
      body: Column(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            SizedBox(height: 20.0,),
            Align(
              alignment: Alignment.centerLeft,
              child: Text(
                'Puertas - Detalles',
                style: kMediumTitleTextStyle,
              ),
            ),
            Container(
              height: 150.0,
              width: double.infinity,
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
                            doorName,
                            style: kLittleGreyTextStyle.copyWith(fontWeight: FontWeight.bold),
                            textAlign: TextAlign.center,
                          ),
                          Text(
                            'Personas dentro: $peopleInside',
                            style: kLittleGreyTextStyle,
                            textAlign: TextAlign.center,
                          ),
                          // SizedBox(height: 10.0,),
                          Text(
                            'Sanitizante: $sanitizer',
                            style: kLittleGreyTextStyle,
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    ),
                    Expanded(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          FittedBox(
                            fit: BoxFit.fitWidth,
                            child: Text(
                              isOpened ? 'Abierta' : 'Cerrada',
                              style: kBigTitleTextStyle.copyWith(fontSize: 30.0),
                              textAlign: TextAlign.center,
                            ),
                          ),
                          FittedBox(
                            fit: BoxFit.fitWidth,
                            child: Card(
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
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
            SizedBox(height: 10.0,),
            Text(
              'Historial - $doorName',
              style: kLittleTitleTextStyle,
            ),
            Divider(thickness: 3,),
            Expanded(
              child: Scrollbar(
                radius: Radius.circular(10.0),
                child: Padding(
                  padding: EdgeInsets.only(right: 15.0),
                  child: ListView.builder(
                    physics: BouncingScrollPhysics(),
                    itemBuilder: (context, index){
                      Log log = logs[index];
                      return DoorLogTile(
                        workerProfileImageUrl: log.workerProfileImage,
                        workerName: log.workerName,
                        email: log.workerEmail,
                        address: log.workerAddress,
                        phoneNumber: log.workerPhoneNumber,
                        doorName: log.doorName,
                        temperature: log.temperature,
                        exitDatetime: log.exitDatetime,
                        entryDatetime: log.entryDatetime,
                        allowed: log.authorized,
                        faceMask: log.faceMask,
                        logImageUrl: log.workerLogImage,
                      );
                    },
                    itemCount: logs.length,
                  )
                ),
              ),
            ),
          ],
        ),
    );
  }
}