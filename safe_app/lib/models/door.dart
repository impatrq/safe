class Door {

  Door({required this.doorName, required this.isOpened, required this.peopleInside, required this.sanitizer, required this.isSafe, required this.logs});

  final String doorName;
  final bool isOpened;
  final int peopleInside;
  final String sanitizer;
  final bool isSafe;
  final List? logs;

}