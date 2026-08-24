import asyncio


async def simulate(nodes):

    print("Machine simulator started.")

    while True:

        # =========================================================
        # READ CURRENT CONTROL VALUES
        # =========================================================

        speed_setpoint = await nodes["speed_setpoint"].read_value()
        temperature_setpoint = await nodes["temperature_setpoint"].read_value()
        pressure_setpoint = await nodes["pressure_setpoint"].read_value()
        flow_rate_setpoint = await nodes["flow_rate_setpoint"].read_value()

        start_command = await nodes["start_command"].read_value()
        stop_command = await nodes["stop_command"].read_value()
        reset_command = await nodes["reset_command"].read_value()

        machine_running = await nodes["machine_running"].read_value()
        fault_active = await nodes["fault_active"].read_value()

        # =========================================================
        # RESET COMMAND
        # =========================================================

        if reset_command:

            await nodes["fault_active"].write_value(False)
            await nodes["emergency_stop"].write_value(False)

            await nodes["high_temperature_alarm"].write_value(False)
            await nodes["high_pressure_alarm"].write_value(False)
            await nodes["motor_overload_alarm"].write_value(False)
            await nodes["low_level_alarm"].write_value(False)
            await nodes["high_vibration_alarm"].write_value(False)

            await nodes["machine_status"].write_value("READY")

            await nodes["reset_command"].write_value(False)

            print("Machine reset.")

        # =========================================================
        # STOP COMMAND
        # =========================================================

        if stop_command:

            await nodes["machine_running"].write_value(False)
            await nodes["motor_running"].write_value(False)

            await nodes["machine_status"].write_value("STOPPED")

            await nodes["motor_speed"].write_value(0.0)

            await nodes["stop_command"].write_value(False)

            print("Machine stopped.")

        # =========================================================
        # START COMMAND
        # =========================================================

        if start_command and not fault_active:

            await nodes["machine_running"].write_value(True)
            await nodes["motor_running"].write_value(True)
            await nodes["machine_ready"].write_value(True)

            await nodes["machine_status"].write_value("RUNNING")

            await nodes["start_command"].write_value(False)

            print("Machine started.")

        # =========================================================
        # READ MACHINE STATE AGAIN
        # =========================================================

        machine_running = await nodes["machine_running"].read_value()
        fault_active = await nodes["fault_active"].read_value()

        # =========================================================
        # MACHINE RUNNING
        # =========================================================

        if machine_running and not fault_active:

            # -----------------------------------------------------
            # Motor
            # -----------------------------------------------------

            current_speed = await nodes["motor_speed"].read_value()

            # Gradually move motor speed toward setpoint
            difference = speed_setpoint - current_speed

            if abs(difference) > 20:
                current_speed += 20 if difference > 0 else -20
            else:
                current_speed = speed_setpoint

            motor_current = 10.0 + (current_speed / 1500.0) * 4.0

            motor_power = (current_speed / 1500.0) * 7.5

            motor_temperature = 60.0 + (
                current_speed / 1500.0
            ) * 15.0

            await nodes["motor_speed"].write_value(
                round(current_speed, 2)
            )

            await nodes["motor_current"].write_value(
                round(motor_current, 2)
            )

            await nodes["motor_power"].write_value(
                round(motor_power, 2)
            )

            await nodes["motor_temperature"].write_value(
                round(motor_temperature, 2)
            )

            await nodes["motor_running"].write_value(True)

            # -----------------------------------------------------
            # Process
            # -----------------------------------------------------

            process_temperature = (
                temperature_setpoint
                + (current_speed - speed_setpoint) * 0.01
            )

            process_pressure = (
                pressure_setpoint
                + (current_speed - speed_setpoint) * 0.001
            )

            flow_rate = (
                flow_rate_setpoint
                * (current_speed / speed_setpoint)
                if speed_setpoint > 0
                else 0
            )

            tank_level = await nodes["tank_level"].read_value()

            # Tank level slowly changes during production
            tank_level += 0.2

            if tank_level > 100:
                tank_level = 60

            vibration = 2.0 + (
                abs(current_speed - speed_setpoint) / 1000
            )

            await nodes["process_temperature"].write_value(
                round(process_temperature, 2)
            )

            await nodes["process_pressure"].write_value(
                round(process_pressure, 2)
            )

            await nodes["flow_rate"].write_value(
                round(flow_rate, 2)
            )

            await nodes["tank_level"].write_value(
                round(tank_level, 2)
            )

            await nodes["vibration"].write_value(
                round(vibration, 2)
            )

            # -----------------------------------------------------
            # Production
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

            await nodes["motor_running"].write_value(False)

            current_speed = await nodes[
                "motor_speed"
            ].read_value()

            # Gradually bring motor speed down
            if current_speed > 0:

                current_speed -= 50

                if current_speed < 0:
                    current_speed = 0

                await nodes["motor_speed"].write_value(
                    current_speed
                )

            await nodes["motor_current"].write_value(0.0)
            await nodes["motor_power"].write_value(0.0)

        # =========================================================
        # ALARM LOGIC
        # =========================================================

        motor_temperature = await nodes[
            "motor_temperature"
        ].read_value()

        process_temperature = await nodes[
            "process_temperature"
        ].read_value()

        process_pressure = await nodes[
            "process_pressure"
        ].read_value()

        tank_level = await nodes[
            "tank_level"
        ].read_value()

        vibration = await nodes[
            "vibration"
        ].read_value()

        # ---------------------------------------------------------
        # High Temperature
        # ---------------------------------------------------------

        high_temperature = (
            process_temperature > temperature_setpoint + 5
        )

        await nodes["high_temperature_alarm"].write_value(
            high_temperature
        )

        # ---------------------------------------------------------
        # High Pressure
        # ---------------------------------------------------------

        high_pressure = (
            process_pressure > pressure_setpoint + 0.5
        )

        await nodes["high_pressure_alarm"].write_value(
            high_pressure
        )

        # ---------------------------------------------------------
        # Motor Overload
        # ---------------------------------------------------------

        motor_current = await nodes[
            "motor_current"
        ].read_value()

        motor_overload = motor_current > 14.0

        await nodes["motor_overload_alarm"].write_value(
            motor_overload
        )

        # ---------------------------------------------------------
        # Low Level
        # ---------------------------------------------------------

        low_level = tank_level < 20

        await nodes["low_level_alarm"].write_value(
            low_level
        )

        # ---------------------------------------------------------
        # High Vibration
        # ---------------------------------------------------------

        high_vibration = vibration > 4.0

        await nodes["high_vibration_alarm"].write_value(
            high_vibration
        )

        # =========================================================
        # OVERALL FAULT
        # =========================================================

        any_alarm = (
            high_temperature
            or high_pressure
            or motor_overload
            or low_level
            or high_vibration
        )

        if any_alarm:

            await nodes["fault_active"].write_value(True)
            await nodes["machine_status"].write_value("ALARM")

            await nodes["machine_running"].write_value(False)
            await nodes["motor_running"].write_value(False)

            print("ALARM detected.")

        # =========================================================
        # WAIT
        # =========================================================

        await asyncio.sleep(2)