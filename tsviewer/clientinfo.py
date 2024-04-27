from dataclasses import dataclass


@dataclass
class ClientInfo:
    """
    Represents the information returned by the clientinfo command
    """
    cid: str
    client_idle_time: str
    client_unique_identifier: str
    client_nickname: str
    client_version: str
    client_platform: str
    client_input_muted: str
    client_output_muted: str
    client_outputonly_muted: str
    client_input_hardware: str
    client_output_hardware: str
    client_default_channel: str
    client_meta_data: str
    client_is_recording: str
    client_version_sign: str
    client_security_hash: str
    client_login_name: str
    client_database_id: str
    client_channel_group_id: str
    client_servergroups: str
    client_created: str
    client_lastconnected: str
    client_totalconnections: str
    client_away: str
    client_away_message: str
    client_type: str
    client_flag_avatar: str
    client_talk_power: str
    client_talk_request: str
    client_talk_request_msg: str
    client_description: str
    client_is_talker: str
    client_month_bytes_uploaded: str
    client_month_bytes_downloaded: str
    client_total_bytes_uploaded: str
    client_total_bytes_downloaded: str
    client_is_priority_speaker: str
    client_nickname_phonetic: str
    client_needed_serverquery_view_power: str
    client_default_token: str
    client_icon_id: str
    client_is_channel_commander: str
    client_country: str
    client_channel_group_inherited_channel_id: str
    client_badges: str
    client_myteamspeak_id: str
    client_integrations: str
    client_myteamspeak_avatar: str
    client_signed_badges: str
    client_base64HashClientUID: str
    connection_filetransfer_bandwidth_sent: str
    connection_filetransfer_bandwidth_received: str
    connection_packets_sent_total: str
    connection_bytes_sent_total: str
    connection_packets_received_total: str
    connection_bytes_received_total: str
    connection_bandwidth_sent_last_second_total: str
    connection_bandwidth_sent_last_minute_total: str
    connection_bandwidth_received_last_second_total: str
    connection_bandwidth_received_last_minute_total: str
    connection_connected_time: str
    connection_client_ip: str
