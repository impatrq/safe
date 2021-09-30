import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:safe_app/utilities/constants.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';

class DoorLogTile extends StatelessWidget {

  DoorLogTile({required this.workerProfileImageUrl, required this.workerName, required this.email, required this.address, required this.phoneNumber, required this.doorName, required this.temperature, required this.exitDatetime, required this.entryDatetime, required this.allowed, required this.faceMask, required this.logImageUrl});

  final String workerProfileImageUrl;
  final String workerName;
  final String email;
  final String address;
  final String phoneNumber;
  final String doorName;
  final String temperature;
  final bool faceMask;
  final String entryDatetime;
  final String exitDatetime;
  final String logImageUrl;
  final bool allowed;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: (){
        Get.bottomSheet(
          Container(
            padding: EdgeInsets.symmetric(vertical: 10.0, horizontal: 20.0),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.only(
                topLeft: Radius.circular(20.0),
                topRight: Radius.circular(20.0),
              ),
            ),
            child: SingleChildScrollView(
              child: Column(
                children: [
                  Container(
                    width: 70.0,
                    height: 3.0,
                    color: Colors.grey,
                  ),
                  Align(
                    alignment: Alignment.centerRight,
                    child: Text(
                      'Empleado',
                      style: kLittleGreyTextStyle,
                    ),
                  ),
                  Divider(
                    thickness: 3,
                    color: Colors.grey[300],
                  ),
                  Row(
                    children: [
                      CircleAvatar(
                        radius: 50.0,
                        backgroundColor: Colors.transparent,
                        backgroundImage: NetworkImage(workerProfileImageUrl),
                      ),
                      SizedBox(width: 10.0,),
                      Expanded(
                        child: Column(
                          children: [
                            Text(
                              workerName,
                              style: kLittleTitleTextStyle,
                              textAlign: TextAlign.center,
                            ),
                            Text(
                              address,
                              style: kLittleGreyTextStyle.copyWith(fontSize: 13.0),
                              textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      ),
                      SizedBox(width: 10.0,),
                      Expanded(
                        child: Column(
                          children: [
                            Text(
                              phoneNumber,
                              style: kLittleGreyTextStyle.copyWith(fontSize: 13.0),
                              textAlign: TextAlign.center,
                            ),
                            Text(
                              email,
                              style: kLittleGreyTextStyle.copyWith(fontSize: 13.0),
                              textAlign: TextAlign.center,
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                  Align(
                    alignment: Alignment.centerRight,
                    child: Text(
                      'Registro',
                      style: kLittleGreyTextStyle,
                    ),
                  ),
                  Divider(
                    thickness: 3,
                    color: Colors.grey[300],
                  ),
                  SizedBox(height: 15.0,),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Container(
                        width: 120.0,
                        height: 120.0,
                        decoration: BoxDecoration(
                          borderRadius: BorderRadius.circular(10.0),
                          image: DecorationImage(
                            fit: BoxFit.cover,
                            image: NetworkImage(logImageUrl)
                          ),
                        ),
                      ),
                      Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Puerta: $doorName',
                            style: kLittleGreyTextStyle.copyWith(color: Colors.black),
                          ),
                          SizedBox(height: 10.0,),
                          Text(
                            'Temperatura: $temperature°',
                            style: kLittleGreyTextStyle.copyWith(color: Colors.black),
                          ),
                          SizedBox(height: 10.0,),
                          Text(
                            'Barbijo: ${faceMask ? 'SI':'NO'}',
                            style: kLittleGreyTextStyle.copyWith(color: Colors.black),
                          ),
                        ],
                      ),
                    ],
                  ),
                  SizedBox(height: 10.0,),
                  Text(
                    allowed ? 'ACCESO PERMITIDO' : 'ACCESO DENEGADO',
                    style: kMediumTitleTextStyle.copyWith(color: allowed ? Colors.green : Colors.red),
                  ),
                  SizedBox(height: 5.0,),
                  Divider(
                    thickness: 3,
                    color: Colors.grey[300],
                  ),
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Expanded(
                          child: Column(
                            children: [
                              Text('Fecha de Entrada', style: kLittleTitleTextStyle.copyWith(fontSize: 14.0),),
                              Text(entryDatetime, style: kLittleGreyTextStyle,),
                            ],
                          )
                      ),
                      Expanded(
                          child: Column(
                            children: [
                              Text('Fecha de Salida', style: kLittleTitleTextStyle.copyWith(fontSize: 14.0),),
                              Text(exitDatetime, style: kLittleGreyTextStyle,),
                            ],
                          )
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
          isScrollControlled: true,
        );
      },
      child: Column(
        children: [
          Row(
            children: [
              CircleAvatar(
                backgroundColor: Colors.transparent,
                backgroundImage: NetworkImage(logImageUrl),
              ),
              Expanded(
                  flex: 4,
                  child: Text(
                    workerName,
                    style: kLittleTitleTextStyle.copyWith(fontSize: 16.0),
                    textAlign: TextAlign.center,
                  )
              ),
              Expanded(
                child: Icon(
                  allowed ? FontAwesomeIcons.checkCircle : FontAwesomeIcons.timesCircle,
                  color: allowed ? Colors.green : Colors.red,
                ),
              ),
              Icon(
                FontAwesomeIcons.ellipsisV,
                color: Color(0xFF333333),
              ),
            ],
          ),
          SizedBox(height: 15.0,),
        ],
      ),
    );
  }
}