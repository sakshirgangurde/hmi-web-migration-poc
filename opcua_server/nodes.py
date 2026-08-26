async def create_nodes(server, idx):

    # Production Line
    production_line = await server.nodes.objects.add_object(
        idx,
        "ProductionLine1")

    machine = await production_line.add_object(
        idx,
        "Machine1")

    # Telemetry
    telemetry = await machine.add_object(
        idx,
        "Telemetry")

    motor_speed = await telemetry.add_variable(
        idx,
        "MotorSpeed",
        1450.0)

    motor_temperature = await telemetry.add_variable(
        idx,
        "MotorTemperature",
        65.0)

    motor_current = await telemetry.add_variable(
        idx,
        "MotorCurrent",
        12.5)

    process_temperature = await telemetry.add_variable(
        idx,
        "ProcessTemperature",
        82.5)

    process_pressure = await telemetry.add_variable(
        idx,
        "ProcessPressure",
        5.2)

    tank_level = await telemetry.add_variable(
        idx,
        "TankLevel",
        72.0)

    vibration = await telemetry.add_variable(
        idx,
        "Vibration",
        2.5)

    flow_rate = await telemetry.add_variable(
        idx,
        "FlowRate",
        120.0)

    motor_power = await telemetry.add_variable(
        idx,
        "MotorPower",
        7.5)

    # Controls

    controls = await machine.add_object(
        idx,
        "Controls")

    speed_setpoint = await controls.add_variable(
        idx,
        "SpeedSetpoint",
        1500.0)

    temperature_setpoint = await controls.add_variable(
        idx,
        "TemperatureSetpoint",
        85.0)

    start_command = await controls.add_variable(
        idx,
        "StartCommand",
        False)

    stop_command = await controls.add_variable(
        idx,
        "StopCommand",
        False)

    # Status

    status = await machine.add_object(
        idx,
        "Status")

    machine_running = await status.add_variable(
        idx,
        "MachineRunning",
        True)

    machine_status = await status.add_variable(
        idx,
        "MachineStatus",
        "RUNNING")

    fault_active = await status.add_variable(
        idx,
        "FaultActive",
        False)

    high_temperature_alarm = await status.add_variable(
        idx,
        "HighTemperatureAlarm",
        False)

    high_pressure_alarm = await status.add_variable(
        idx,
        "HighPressureAlarm",
        False)

    production_count = await status.add_variable(
        idx,
        "ProductionCount",
        1250)

    # Writable Variables

    writable_variables = [
        speed_setpoint,
        temperature_setpoint,
        start_command,
        stop_command,
    ]

    for variable in writable_variables:
        await variable.set_writable()

    # Return Node References

    return {
        # Telemetry
        "motor_speed": motor_speed,
        "motor_temperature": motor_temperature,
        "motor_current": motor_current,
        "process_temperature": process_temperature,
        "process_pressure": process_pressure,
        "tank_level": tank_level,
        "vibration": vibration,
        "flow_rate": flow_rate,
        "motor_power": motor_power,

        # Controls
        "speed_setpoint": speed_setpoint,
        "temperature_setpoint": temperature_setpoint,
        "start_command": start_command,
        "stop_command": stop_command,

        # Status
        "machine_running": machine_running,
        "machine_status": machine_status,
        "fault_active": fault_active,
        "high_temperature_alarm": high_temperature_alarm,
        "high_pressure_alarm": high_pressure_alarm,
        "production_count": production_count,
    }