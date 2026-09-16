import 'package:elderly_app/main.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  testWidgets('Elderly app smoke test verifies title and buttons', (
    WidgetTester tester,
  ) async {
    await tester.pumpWidget(const MindCareApp());

    // Verify app title and greeting
    expect(find.text('MINDCARE'), findsOneWidget);
    expect(find.text('Good Morning! 🌸'), findsOneWidget);
    expect(find.text('Memory Match Game'), findsOneWidget);
    expect(find.text('Reminders & Health'), findsOneWidget);
    expect(find.text('Voice Assistant'), findsOneWidget);
  });
}
