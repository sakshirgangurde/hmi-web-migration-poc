import asyncio
import random


async def simulate(nodes):

    print("Machine simulator started.")

    while True:

        # =========================================================
        # READ CONTROL VALUES
        # =========================================================

        speed_setpoint = await nodes[
            "speed_setpoint"
        ].read_value()

        temperature_setpoint = await nodes[
            "temperature_setpoint"
        ].read_value()

        start_command = await nodes[
            "start_command"
        ].read_value()

        stop_command = await nodes[
            "stop_command"
        ].read_value()

        # =========================================================
        # START COMMAND
        # =========================================================

        if start_command:

            await nodes["machine_running"].write_value(True)
            await nodes["machine_status"].write_value("RUNNING")

            await nodes["start_command"].write_value(False)

            print("Machine started.")

        # =========================================================
        # STOP COMMAND
        # =========================================================

        if stop_command:

            await nodes["machine_running"].write_value(False)
            await nodes["machine_status"].write_value("STOPPED")

            await nodes["stop_command"].write_value(False)

            print("Machine stopped.")

        # =========================================================
        # READ MACHINE STATE
        # =========================================================

        machine_running = await nodes[
            "machine_running"
        ].read_value()

        fault_active = await nodes[
            "fault_active"
        ].read_value()

        # =========================================================
        # MACHINE RUNNING
        # =========================================================

        if machine_running and not fault_active:

            # -----------------------------------------------------
            # Motor Speed
            # -----------------------------------------------------

            current_speed = await nodes[
                "motor_speed"
            ].read_value()

            difference = speed_setpoint - current_speed

            # Gradually move motor speed toward setpoint
            if abs(difference) > 20:

                current_speed += (
                    20 if difference > 0 else -20
                )

            else:

                current_speed = speed_setpoint

            await nodes["motor_speed"].write_value(
                round(current_speed, 2)
            )

            # -----------------------------------------------------
            # Motor Current
            # -----------------------------------------------------

            base_current = (
                10.0
                + (current_speed / 1500.0) * 4.0
            )

            motor_current = (
                base_current
                + random.uniform(-0.3, 0.3)
            )

            await nodes["motor_current"].write_value(
                round(motor_current, 2)
            )

            # -----------------------------------------------------
            # Motor Power
            # -----------------------------------------------------

            base_power = (
                current_speed / 1500.0
            ) * 7.5

            motor_power = (
                base_power
                + random.uniform(-0.15, 0.15)
            )

            await nodes["motor_power"].write_value(
                round(max(0, motor_power), 2)
            )

            # -----------------------------------------------------
            # Motor Temperature
            # -----------------------------------------------------

            base_motor_temperature = (
                60.0
                + (current_speed / 1500.0) * 15.0
            )

            motor_temperature = (
                base_motor_temperature
                + random.uniform(-1.0, 1.0)
            )

            await nodes["motor_temperature"].write_value(
                round(motor_temperature, 2)
            )

            # -----------------------------------------------------
            # Process Temperature
            # -----------------------------------------------------

            base_process_temperature = (
                temperature_setpoint
                + (current_speed - speed_setpoint) * 0.01
            )

            process_temperature = (
                base_process_temperature
                + random.uniform(-1.0, 1.0)
            )

            await nodes["process_temperature"].write_value(
                round(process_temperature, 2)
            )

            # -----------------------------------------------------
            # Process Pressure
            # -----------------------------------------------------

            base_pressure = (
                5.0
                + (current_speed / 1500.0) * 0.5
            )

            process_pressure = (
                base_pressure
                + random.uniform(-0.08, 0.08)
            )

            await nodes["process_pressure"].write_value(
                round(process_pressure, 2)
            )

            # -----------------------------------------------------
            # Flow Rate
            # -----------------------------------------------------

            base_flow = (
                120.0
                * (current_speed / 1500.0)
            )

            flow_rate = (
                base_flow
                + random.uniform(-2.0, 2.0)
            )

            await nodes["flow_rate"].write_value(
                round(max(0, flow_rate), 2)
            )

            # -----------------------------------------------------
            # Tank Level
            # -----------------------------------------------------

            tank_level = await nodes[
                "tank_level"
            ].read_value()

            tank_level += random.uniform(0.1, 0.3)

            if tank_level > 100:
                tank_level = 60

            await nodes["tank_level"].write_value(
                round(tank_level, 2)
            )

            # -----------------------------------------------------
            # Vibration
            # -----------------------------------------------------

            base_vibration = (
                2.0
                + abs(current_speed - speed_setpoint) / 1000
            )

            vibration = (
                base_vibration
                + random.uniform(-0.2, 0.2)
            )

            await nodes["vibration"].write_value(
                round(max(0, vibration), 2)
            )

            # -----------------------------------------------------
            # Production Count
            # -----------------------------------------------------

            production_count = await nodes[
                "production_count"
            ].read_value()

            production_count += 1

            await nodes["production_count"].write_value(
                production_count
            )

        # =========================================================
        # MACHINE STOPPED
        # =========================================================

        else:

            current_speed = await nodes[
                "motor_speed"
            ].read_value()

            # Gradually reduce motor speed
            if current_speed > 0:

                current_speed -= 50

                if current_speed < 0:
                    current_speed = 0

                await nodes["motor_speed"].write_value(
                    current_speed
                )

            # Motor values go to zero when stopped
            await nodes["motor_current"].write_value(0.0)
            await nodes["motor_power"].write_value(0.0)

        # =========================================================
        # ALARM LOGIC
        # =========================================================

        process_temperature = await nodes[
            "process_temperature"
        ].read_value()

        process_pressure = await nodes[
            "process_pressure"
        ].read_value()

        # ---------------------------------------------------------
        # High Temperature Alarm
        # ---------------------------------------------------------

        high_temperature = (
            process_temperature
            > temperature_setpoint + 5
        )

        await nodes[
            "high_temperature_alarm"
        ].write_value(high_temperature)

        # ---------------------------------------------------------
        # High Pressure Alarm
        # ---------------------------------------------------------

        high_pressure = (
            process_pressure > 5.7
        )

        await nodes[
            "high_pressure_alarm"
        ].write_value(high_pressure)

        # OVERALL FAULT

        any_alarm = (
            high_temperature
            or high_pressure
        )

        if any_alarm:

            await nodes[
                "fault_active"
            ].write_value(True)

            await nodes[
                "machine_status"
            ].write_value("ALARM")

            await nodes[
                "machine_running"
            ].write_value(False)

            print("ALARM detected.")

        else:

            await nodes[
                "fault_active"
            ].write_value(False)

        # WAIT
        await asyncio.sleep(2)