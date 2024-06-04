import requests

from test_sdkbase import TestSdk
import ragflow
from ragflow.ragflow import RAGFLow
import pytest
from unittest.mock import MagicMock, Mock


class TestCase(TestSdk):

    @pytest.fixture
    def ragflow_instance(self):
        # Here we create a mock instance of RAGFlow for testing
        return ragflow.ragflow.RAGFLow('123', 'url')

    def test_version(self):
        print(ragflow.__version__)

    def test_create_dataset(mocker):
        # 设置模拟的请求响应
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"name": "abc", "id": 123}

        # 使用 pytest-mock 模拟 requests.post 方法
        mocker.patch('requests.post', return_value=mock_response)

        # 实例化 RAGFLow 类
        ragflow = RAGFLow(user_key='user_key', base_url='http://example.com')

        # 调用方法
        result = ragflow.create_dataset('dataset1')

        # 检查结果
        assert result == {"Name": "abc", "Id": 123}

        # 检查 requests.post 是否被调用
        requests.post.assert_called_once_with('http://example.com/api/v1/dataset', json={"name": "dataset1"})

    def test_delete_dataset(self):
        assert ragflow.ragflow.RAGFLow('123', 'url').delete_dataset('abc') == 'abc'

    def test_list_dataset_success(self, ragflow_instance, monkeypatch):
        # Mocking the response of requests.get method
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'datasets': [{'id': 1, 'name': 'dataset1'}, {'id': 2, 'name': 'dataset2'}]}

        # Patching requests.get to return the mock_response
        monkeypatch.setattr("requests.get", MagicMock(return_value=mock_response))

        # Call the method under test
        result = ragflow_instance.list_dataset()

        # Assertion
        assert result == [{'id': 1, 'name': 'dataset1'}, {'id': 2, 'name': 'dataset2'}]

    def test_list_dataset_failure(self, ragflow_instance, monkeypatch):
        # Mocking the response of requests.get method
        mock_response = MagicMock()
        mock_response.status_code = 404  # Simulating a failed request

        # Patching requests.get to return the mock_response
        monkeypatch.setattr("requests.get", MagicMock(return_value=mock_response))

        # Call the method under test
        result = ragflow_instance.list_dataset()

        # Assertion
        assert result is None
